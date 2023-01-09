from telethon.tl.custom import Button

def main_markup():  
    markup = [
            [Button.inline("פרופיל אישי",'user_profile')],
            [Button.inline("חיפוש",'serch')],
            [Button.inline("הוספת פוסט",'add_post')],
            [Button.inline("פוסטים לפי אזור",'post_by_area')],
            [Button.inline("פוסטים שלי",'my_posts')],
            [Button.inline("היסטורית הסמנות",'order_history')]         
        ]
    return markup


# def main_markup():  
#     d='add-photo:{}:{}' 
#     markup = [
#             [Button.inline("nbv 1",d.format(1))],
#             [Button.inline("nbv 2",d.format(2))],
#             [Button.inline("הוספת פוסט",'add_post')],
#             [Button.inline("פוסטים לפי אזור",'post_by_area')],
#             [Button.inline("היסטורית הסמנות",'order_history')]         
#         ]
#     return markup
