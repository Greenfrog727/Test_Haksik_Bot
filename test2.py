import requests
from bs4 import BeautifulSoup
import datetime

현재시각 = str(datetime.datetime.now())
#print(현재시각)
yyyy = 현재시각[:4]
mm = 현재시각[5:7]
dd = 현재시각[8:10]
date =  yyyy + "-" + mm + "-" + dd
days = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
요일 = days[datetime.date(int(yyyy, 16), int(mm, 16), int(dd, 16)).weekday()]
#print(date)

req = requests.get("https://mini.snu.ac.kr/index.php/cafe/set/" + date)
soup = BeautifulSoup(req.text, "html.parser")

table_div = soup.find(id="main")
#table_body = table_div.find('tbody')
table_menu = table_div.find_all('tr')
lunch_menu_table_301 = table_menu[13]
lunch_menu_table_302 = table_menu[14]
dinner_menu_table_302 = table_menu[24]

lunch_301 = (lunch_menu_table_301.find('td', class_="menu"))
lunch_302 = (lunch_menu_table_302.find('td', class_="menu"))
dinner_302 =(dinner_menu_table_302.find('td', class_="menu"))

점심_301동 = ""
for i in lunch_301:
    점심_301동 = 점심_301동 + i.text + "\n"

점심_302동 = ""
for i in lunch_302:
    점심_302동 = 점심_302동 + i.text + "\n"

저녁_302동 = ""
for i in dinner_302:
    저녁_302동 = 저녁_302동 + i.text + "\n"

#print(저녁_302동)

import telegram
from telegram import InlineKeyboardButton as btn, InlineKeyboardMarkup as mu, ChatAction
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

토큰 = "5139847352:AAGQqdYdiMjqdh1JDEqLUzzkZAfXsQCRHbM"
bot = telegram.Bot(token = 토큰)
updater = Updater(token = 토큰)
# for i in bot.getUpdates():
#     print(i.message)
chat_id = 1772638862

bot.send_message(chat_id, mm + "월" + dd + "일 " + 요일 + "\n<봄이온 소반 301동> 점심\n\n" + 점심_301동)
bot.send_message(chat_id, mm + "월" + dd + "일 " + 요일 + "\n<302동 식당> 점심\n\n" + 점심_302동)
bot.send_message(chat_id, mm + "월" + dd + "일 " + 요일 + "\n<302동 식당> 저녁\n\n" + 저녁_302동)
    
updater.start_polling()
updater.idle()