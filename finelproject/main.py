import asyncio
from telethon import events
import init_db as database
from telethon.sync import TelegramClient
from os import path
from tables import *
import sys
from settings import bot
from buttons import *
from manage_user import *
from utils import *

initDbFlag=False

@bot.on(events.NewMessage)
async def message1(event):
    print(event)
    print("_-------------------------------------------------------------0-----")
    #print(event)
    sender = await event.get_sender()
    print(event.from_id)
    sender = sender.id
    print(sender)
    await delet_all_messages(sender ,event)
    if event.message.message == "/start":
        print("kakkakakakkakakkak=+++++++")
        helper = await UserEventHelper(event,sender,event.from_id).manage.init_()
        #helper = await UserEventHelper(event,sender).manage.message_sender("אנא בחר",markup= main_markup())
    else:
        
        help =  UserEventHelper(event,sender,event.from_id)

        #await help.runner("delet_all_messages")
        await help.runner('message')
    

@bot.on(events.CallbackQuery)
async def callback(event):
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"777777{event}")
    sender = await event.get_sender()
    
    sender = sender.id
    print(f"88888{sender}")
    help =  UserEventHelper(event,sender)
    #await help.runner("delet_all_messages")
    await delet_all_messages(sender ,event)
    await help.runner('callback_query')
    

async def delete1(event,sender):
    async for message in bot.iter_messages(event.chat_id, from_user='me'):
        #bot.delete_messages(sender, message.id)
        print(f"qqqqqqwwwwwww{message}")
# @bot.on(events.NewMessage(pattern='/(?i)Start'))
# async def message1(event):
# #    await database.init()
    
#     print(f"------------------------{event.message.message}")
#     sender = await event.get_sender()
#     sender = sender.id
#     # check =check_user(sender)
#     # if check==None:
#     #     await user_registration(event,sender)
#     await UserEventHelper(event,sender).manage.init_()

class UserEventHelper:

    def __init__(self, event,sender,from_id=None):
        print("3")
        # print('Client:', event.stringify())
        # stg.logger.info(event)
        
        self.manage = Manage_User(event,sender,from_id)
        #Manage_User(event,sender)
        print("4")
        return None

    async def runner(self, func):
        try:
            print("5")
            check = await self.manage.init_()
            print(f"lllllllll{check}")
            if check != None:
                await getattr(self.manage, func)()
        except Exception as e:
            print(f"from user event helper:{e} ")
            
async def main():
    print("trying to create database")
    await database.init()
    print("database is created")
    await asyncio.gather(bot.run_until_disconnected())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    while True:
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            exit()
        except Exception:
            print("problem whit main")

#bot.run_until_disconnected()
async def check_user(sender):
    user =await User.filter(id = sender)
    return user

async def user_registration(event,sender):
    user =await User(id = sender , flow = "user_registration_first_name").save()
    await UserEventHelper(event,sender).manage.message_sender("ברוך הבא לtelecar בוט השכרת הרכב הטוב ביותר. מה שנשאר זה רק להרשם\n נא לשלוח הודעת טקסט עם שמך")
    
    # call messaes of the user
