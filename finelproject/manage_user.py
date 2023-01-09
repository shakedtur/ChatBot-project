
from ast import Break
import os
from typing import Final
from telethon import types
import telethon
from random import choices
import time
import asyncio
from telethon.tl.functions.users import GetFullUserRequest
from telethon import events
from telethon.sync import TelegramClient
from telethon.tl.custom import Button
from tables import *
from buttons import *
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.types import InputMessagesFilterEmpty
from text import *
from settings import *

class Manage_User():

    def __init__(self, event,sender,from_id =None):
        print("1")
        self.event = event

        print(f"------{sender}")
    #    sender = sender.id
        #self.sender = await event.get_sender().id
        self.sender = sender
        self.chat_id = event.chat_id
        self.user_db = None
        self.post_in_work = None
        self.from_id = from_id
        
        try:
            self.text = self.event.text
        except AttributeError:
            self.text = None
#        self.entities = event.message.entities
        return None
    async def init_(self):
        if self.from_id !=None:
            return None
        try:
            user =await User.filter(id = self.sender).first()
            print(f"ppppppppppppppp{self.sender}")
            print(f"::::{user}")
            if user == None:
                self.user_db = await User(id = self.sender , flow = "user_registration_first_name").save()
                await self.message_sender("ברוך הבא לtelecar בוט השכרת הרכב הטוב ביותר. מה שנשאר זה רק להרשם\n נא לשלוח הודעת טקסט עם שמך")
                return True
                
            else:
                self.user_db=user
                return True
                
        except AttributeError as e:
            print(f"problem whit init_{e}")
            return None
        



    async def message(self):
        #print(f"pppppp{self.sender}")
        print(12)
        if self.event.message.is_private:
            print(13)
            await self.private_message()
            return
#send the message and buttons and save in db (after callback this message will be deleted )
    async def message_sender(self,message,markup=None):
        #bot.edit_message(SENDER,messsage_to_edit,orderContentIngredients.format(pageMeals[index].content,pageMeals[index].Ingredients),file= pageMeals[index].photoPath ,buttons=buttons)
        if markup is None:
            m = await self.event.respond(message)
        else:
            m = await self.event.respond( message ,buttons = markup)
        await self.save_all_lest_messag([m.id])      
        
    async def private_message(self):
        if self.user_db.flow == "user_registration_first_name":
            print(f"text++++++++++++++++++{self.text}")
            self.user_db.first_name = self.text
            self.user_db.flow= "user_registration_last_name"
            await self.user_db.save()
            await self.message_sender("מצויין עכשיו נא לשלוח את שם המשפחה בהודעת טקסט")
            print(self.text)
            
        elif self.user_db.flow == "user_registration_last_name":
            self.user_db.last_name = self.text
            self.user_db.flow= "user_registration_email"
            await self.user_db.save()
            await self.message_sender("מצויין עכשיו נא לשלוח את שם האימייל בהודעת טקסט")
            
        elif self.user_db.flow == "user_registration_email":
            self.user_db.email = self.text
            self.user_db.flow= "user_registration_phone_number"
            await self.user_db.save()
            await self.message_sender("מצויין עכשיו נא לשלוח את מספר הטלפון בהודעת טקסט")
            
        elif self.user_db.flow == "user_registration_phone_number":
            self.user_db.phone_number = self.text
            self.user_db.flow= None
            await self.user_db.save()
            a= User().filter(id = self.sender)
            print(f"++TT{a}")
            await self.message_sender("ההרשמה הסתיימה בהצלחה!! \n  ברוך הבא לtelecar",markup=main_markup())
            
        elif "add_post" in self.user_db.flow:
            step=self.user_db.flow.split(":")
            await self.add_post(step[1])
            
        else:
            await self.message_sender("הודעתך נקלטה אך המערכת לא מחכה להודעות \n אנא בחר",main_markup())

    #save list of message ids in the db     
    async def save_all_lest_messag(self,m_ids):
        try:
            for m_id in m_ids:
                newMessage = UserMessages(id = m_id , user_id = self.sender )
                await newMessage.save()
        except Exception as e:
            await self.event.respond('Error loading func save_all_lest_messag please try again::', parse_mode='html' ,buttons=main_markup())
            print("'Error loading func save_all_lest_messag please try again::",e)

    async def user_profile(self,flow = None):
        pass
    async def my_posts(self,flow = None):
        pass
                
    async def add_post(self,flow = None):
        print("ww")
        if flow is None:
            try:
                print(f"22222{self.sender}")
                self.post_in_work = await Post(owner_id=self.sender).save()
                print("xx")
                self.user_db.flow= "add_post:car_company"
                await self.user_db.save()
                await self.message_sender("נא להוסיף את שם חברת הרכב . לדוגמא יונדאי,פורד וכדומה")
            except Exception as e:
                print(f"eror in add_post flow=none :{e}")
        
        elif flow == "car_company":
            try:
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.car_type = self.text
                await self.post_in_work.save()
                self.user_db.flow= "add_post:car_model"
                await self.user_db.save()
                await self.message_sender("נא להוסיף את שם הדגם של הרכב ")
            except Exception as e:
                print(f"eror in add_post flow=none :{e}")

        elif flow == "car_type":
            try:
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.car_type = self.text
                await self.post_in_work.save()
                self.user_db.flow= "add_post:car_model"
                await self.user_db.save()
                await self.message_sender("נא להוסיף את שם הדגם של הרכב ")    
            except Exception as e:
                print(f"eror in add_post flow=car_type :{e}")
            
            
        # elif flow == "car_name":
        #     self.post_in_work.car_type = self.text
        #     await self.post_in_work.save()
        #     self.user_db.flow= "add_post:car_company"
        #     await self.user_db.save()
        #     await self.message_sender("נא להוסיף את שם חברת הרכב . לדוגמא יונדאי,פורד וכדומה")
        
        elif flow == "car_model":
            try:
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.car_model = self.text
                await self.post_in_work.save()
                self.user_db.flow= "add_post:car_production_year"
                await self.user_db.save()
                await self.message_sender("נא להוסיף את שם הדגם של הרכב")
            except Exception as e:
                print(f"eror in add_post flow=car_model :{e}")
            
        
        elif flow == "car_production_year":
            try:
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.car_production_year = self.text
                await self.post_in_work.save()
                self.user_db.flow= "add_post:Engine_capacity"
                await self.user_db.save()
                await self.message_sender("נא להוסיף את הנפח המנוע בליטרים")
            except Exception as e:
                print(f"eror in add_post flow=car_production_year :{e}")
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.car_production_year = self.text
                await self.post_in_work.save()
                self.user_db.flow= "add_post:Engine_capacity"
                await self.user_db.save()
                await self.message_sender("נא להוסיף את הנפח המנוע בליטרים")
            
        elif flow == "Engine_capacity":
            try:
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.Engine_capacity = self.text
                await self.post_in_work.save()
                self.user_db.flow= "add_post:horsepower"
                await self.user_db.save()
                await self.message_sender("נא להוסיף את כוחות הסוס של הרכב ")
            except Exception as e:
                print(f"eror in add_post flow=Engine_capacity :{e}")
            
            
        elif flow == "horsepower":
            try:
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.horsepower = self.text
                await self.post_in_work.save()
                self.user_db.flow= "add_post:txt_content"
                await self.user_db.save()
                await self.message_sender("נא להוסיף תוכן הפוסט")
            except Exception as e:
                print(f"eror in add_post flow=horsepower :{e}")
            
            
        elif flow == "txt_content":
            try:
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.txt_content = self.text
                await self.post_in_work.save()
                self.user_db.flow= "add_post:km"
                await self.user_db.save()
                await self.message_sender("נא להוסיף את הקילומטרז של הרכב")
            except Exception as e:
                print(f"eror in add_post flow=txt_content :{e}")
                
            
        elif flow == "km":
            try:
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.km = self.text
                await self.post_in_work.save()
                self.user_db.flow= "add_post:address"
                await self.user_db.save()
                await self.message_sender("נא להוסיף כתובת לאיסוף")
            except Exception as e:
                print(f"eror in add_post flow=km :{e}")
            
            
        elif flow == "address":
            try:
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.address = self.text
                await self.post_in_work.save()
                self.user_db.flow= "add_post:phone_number"
                await self.user_db.save()
                await self.message_sender("נא להוסיף את מספר הטלפון")    
            except Exception as e:
                print(f"eror in add_post flow=address :{e}")
            
            
        elif flow == "phone_number":
            try:
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.phone_number = self.text
                await self.post_in_work.save()
                self.user_db.flow= "add_post:cost"
                await self.user_db.save()
                await self.message_sender("נא להוסיף אתה מחיר השכרת רכב פר יום")    
            except Exception as e:
                print(f"eror in add_post flow=phone_number :{e}")
            
            
            
        elif flow == "cost":
            try:
                self.post_in_work = await Post().filter(owner_id=self.sender).first()
                self.post_in_work.cost = self.text
                self.post_in_work.data_is_full = True
                await self.post_in_work.save()
                self.user_db.flow= None
                await self.user_db.save()
                await self.message_sender("הפוסט שלך פורסם בהצלחה ניתן יהיה לראות אותו בפוסטים שלי",markup=main_markup())   
            except Exception as e:
                print(f"eror in add_post flow=cost :{e}")
                self.post_in_work.cost= None
                self.post_in_work.data_is_full = False
                self.post_in_work.save()
                self.user_db.flow= "add_post:cost"
                self.user_db.save()
                await self.message_sender("משהו השתבש בהכנסת המכיר אנא נסו שוב")
                    
                
            
            
            
        
    """    car_company = fields.CharField(max_length=50, null=True)
    car_type = fields.CharField(max_length=50, null=True)
    car_name = fields.CharField(max_length=50, null=True)
    car_model = fields.CharField(max_length=50, null=True)
    car_type = fields.CharField(max_length=50, null=True)
    car_production_year = fields.CharField(max_length=20, null=True)
    Engine_capacity = fields.CharField(max_length=20, null=True)
    horsepower = fields.CharField(max_length=20, null=True)
    photo_path = fields.TextField( null = True)
    from_date= fields.DatetimeField(auto_now_add=True) 
    to_date= fields.DatetimeField(auto_now_add=True) 
    txt_content= fields.CharField(max_length=200, null = True, unique= False)
    km = fields.IntField(default = 0)
    address = fields.CharField(max_length=40, null = True, unique= False)
    phone_number = fields.IntField(null = True, unique= False)
    date_and_time = fields.DatetimeField(auto_now_add=True)
    owner: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="posts_as_owner" , to_field = "id"
    )
    renter: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="posts_as_renter" , to_field = "id"
    )
    cost = fields.IntField(null=True)"""
    async def main_window(self):
        await self.message_sender("אנא בחר ",main_markup())
        
    async def callback_query(self):
        try:
            data = self.event.data.decode("utf-8").split(':')
            if len(data) > 1:
                await getattr(self, data[0])(*data[1:])
            else:
                await getattr(self, data[0])()
        except Exception:
            print("problem whit callback query" )
            
        print(f"2222222222{data}")
        
