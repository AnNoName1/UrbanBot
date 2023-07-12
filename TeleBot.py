#!/usr/bin/env python
# coding: utf-8

# token is "token here"

# In[ ]:


get_ipython().system('pip3 install pytelegrambotapi')


# In[ ]:


get_ipython().system('pip3 install bs4')
#else:
#   bot.send_message(message.from_user.id, parse_html(message.text))


# In[ ]:


import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
bot = telebot.TeleBot('"token here"')

@bot.message_handler(commands=['start'])

def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Start")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Hello I am UrbanBot", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == 'Start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        bot.send_message(message.from_user.id, 'bot can provide definition to english/american slang as well as links to related terms') #ответ бота
    else:
        result, links = parse_html(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for link in links:
            markup.add(types.KeyboardButton(link))
        
        bot.send_message(message.from_user.id, result, reply_markup=markup)


bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть


# In[ ]:


def parse_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    url = 'https://www.urbandictionary.com/define.php?term='+ html_text
    response = requests.get(url)
    bs = BeautifulSoup(response.text,"lxml")
    term = bs.find('a', class_='word text-denim font-bold font-serif dark:text-fluorescent break-all text-3xl md:text-[2.75rem] md:leading-10')
    meaning = bs.find('div', class_='break-words meaning mb-4')
    if(meaning):
        links = meaning.find_all('a', class_='autolink')
        result = str(term.text + " - " + meaning.text)
        link_texts = [link.text.strip() for link in links]
        return result, link_texts
    else:
        return "nothing found",["nothing"]






