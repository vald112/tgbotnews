#!/bin/python3

import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import sqlite3
import telebot
from telebot import types
import os

bot = telebot.TeleBot("ТОКЕН")
@bot.message_handler(commands=['s'])
def send_message(message):
    chat_id = message.chat.id
    bot.send_message(ID_ЧАТА, 'Привет, я буду говорить тебе, когда появятся свежие новости в посольстве Чешской Республики в Москве')


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'}
url = 'https://www.mzv.cz/moscow/ru/vizy_i_konsulskaja/novosti/index.html'

db = sqlite3.connect("newsbot.db")
cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS czech (
    ID INTEGER PRIMARY KEY,
    NAME TEXT
)""")

v = []
ra = []
#выгрузка с базы данных с преобразование в список
value = list(cur.execute('''SELECT NAME FROM czech'''))
for row in value:
    v.append(row[0])
print(type(v))
print(v)

#парсим данные с сайта
p = requests.get(url)
w = bs(p.text, "lxml")

result_list = []
name_list = [] 
           
#результат парсинга 
for results in w.find_all('h2', class_='article_title'):
    r = results.find('a').text.strip()
    ra.append(r)
#print(type(ra), ra)

#сравнение данных
res = [x for x in ra + v if x not in ra or x not in v]
if not res:
    print('Нет новых новостей в Чешском посольстве')
    bot.send_message(ID_ЧАТА, Нет новых новостей в Чешском посольстве\nhttps://www.mzv.cz/moscow/ru/vizy_i_konsulskaja/novosti/index.html')
else:
#    print(res,type(res)) 
    cur.execute("""DROP TABLE czech""")
    db = sqlite3.connect("newsbot.db")
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS czech (
        ID INTEGER PRIMARY KEY,
        NAME TEXT
    )""")
    for i in w.find_all('h2', class_='article_title'):
        list = i.find('a').text.strip()
        name_list.append(list)
#    print(name_list)

    i = 0
    while i < len(name_list):
        name1 = name_list[i]

        cur.execute("""INSERT INTO czech (NAME) VALUES (?);""", (name1,))
        db.commit()
        print("Добавлено " + str(i))
        i = i + 1
    res = '.\n\n'.join(res)
    text = 'Есть новая новость! \nСписок со страницы посольства Чехии\nhttps://www.mzv.cz/moscow/ru/vizy_i_konsulskaja/novosti/index.html\n\n' + str(res)
    bot.send_message(ID_ЧАТА, text)
    print('Отправил уведомление')
