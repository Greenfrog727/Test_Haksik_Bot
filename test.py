import requests
from bs4 import BeautifulSoup
import datetime

현재시각 = str(datetime.datetime.now())
#print(현재시각)
yyyy = 현재시각[:4]
mm = 현재시각[5:7]
dd = 현재시각[8:10]
date =  mm + "/" + dd + "/" + yyyy
days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
요일 = days[datetime.date(int(yyyy, 16), int(mm, 16), int(dd, 16)).weekday()]
#print(날짜)

#req = requests.get("https://snuco.snu.ac.kr/ko/foodmenu?field_menu_date_value_1%5Bvalue%5D%5Bdate%5D=&field_menu_date_value%5Bvalue%5D%5Bdate%5D=" + mm + "%2F" + dd + "%2F" + yyyy + "/")
req = requests.get("https://snuco.snu.ac.kr/ko/foodmenu?field_menu_date_value_1%5Bvalue%5D%5Bdate%5D=&field_menu_date_value%5Bvalue%5D%5Bdate%5D=04%2F11%2F2022")
#print(req.text)
soup = BeautifulSoup(req.text, "html.parser")
#print(soup)

table_div = soup.find('div', class_="view-content")
table = table_div.find('table', class_="views-table cols-4")
table_body = table.find('tbody')
table_menu = table_body.find_all('tr')
menu_table_302 = table_menu[10]
menu_table_301 = table_menu[11]

lunch_302 = menu_table_302.find('td', class_="views-field views-field-field-lunch")
lunch_301 = menu_table_301.find('td', class_="views-field views-field-field-lunch")

dinner_302 = menu_table_302.find('td', class_="views-field views-field-field-dinner")
dinner_301 = menu_table_301.find('td', class_="views-field views-field-field-dinner")

lunch_302 = lunch_302.find_all('p')
lunch_301 = lunch_301.find_all('p')

dinner_302 = dinner_302.find_all('p')
#dinner_301 = dinner_301.find('p')

점심_302동 = ""
for i in lunch_302:
    점심_302동 = 점심_302동 + i.text + "\n"
# print("<302동 점심>")
# print()
# print(점심_302동)
# print()

점심_301동 = ""
for i in lunch_301:
    점심_301동 = 점심_301동 + i.text + "\n"
# print("<301동 점심>")
# print()
# print(점심_301동)
# print()

저녁_302동 = ""
for i in dinner_302:
    저녁_302동 = 저녁_302동 + i.text + "\n"
# print("<302동 저녁>")
# print()
# print(저녁_302동)
# print()

import telegram
from telegram import InlineKeyboardButton as btn, InlineKeyboardMarkup as mu, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

토큰 = "5139847352:AAGQqdYdiMjqdh1JDEqLUzzkZAfXsQCRHbM"
bot = telegram.Bot(token = 토큰)
updater = Updater(token = 토큰)
#for i in bot.getUpdates():
#    print(i.message)
chat_id = bot.getUpdates()[-1].message.chat.id

# try :
#     bot.send_message(chat_id = chat_id, text = 점심_301동)
# except : 
#     pass

def cmd_task_buttons(update, context):
    task_buttons = [
        [btn('301동 점심', callback_data=1 )],
        [btn('302동 점심', callback_data=2 )], 
        [btn('302동 저녁', callback_data=3 )], 
        [btn('종료', callback_data=9 )]
    ]
    
    reply_markup = mu(task_buttons)
    
    context.bot.send_message(
        chat_id=update.message.chat_id
        , text="원하는 식단을 선택해주세요."
        , reply_markup=reply_markup
    )
 
def cb_button(update, context):
    query = update.callback_query
    data = query.data
    
    context.bot.send_chat_action(
        chat_id=update.effective_user.id
        , action=ChatAction.TYPING
    )
    
    if data == '9':
        context.bot.edit_message_text(
            text="종료되었습니다."
            , chat_id=query.message.chat_id
            , message_id=query.message.message_id
        )
    else:
        if data == '1' and 요일 != '토요일' and 요일 != '일요일':
            context.bot.edit_message_text(
            text= mm + "월 " + dd + "일 " + 요일 + " " + "\n" + "<301동 봄이온 소반> 점심" + "\n\n" + 점심_301동
            , chat_id=query.message.chat_id
            , message_id=query.message.message_id
        )
        elif data == '2' and 요일 != '토요일' and 요일 != '일요일':
            context.bot.edit_message_text(
            text= mm + "월 " + dd + "일 " + 요일 + " " + "\n" + "<302동 식당> 점심" + "\n\n" + 점심_302동
            , chat_id=query.message.chat_id
            , message_id=query.message.message_id
        )
        elif data == '3' and 요일 != '토요일' and 요일 != '일요일':
            context.bot.edit_message_text(
            text= mm + "월 " + dd + "일 " + 요일 + " " + "\n" + "<302동 식당> 저녁" + "\n\n" + 저녁_302동
            , chat_id=query.message.chat_id
            , message_id=query.message.message_id
        )
        
    
 
def add_handler(cmd, func):
        updater.dispatcher.add_handler(CommandHandler(cmd, func))
 
add_handler('task', cmd_task_buttons)
 
def callbsck_handler(func):
        updater.dispatcher.add_handler(CallbackQueryHandler(func))
 
callbsck_handler(cb_button)
 
updater.start_polling()
updater.idle()