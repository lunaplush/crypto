import telebot
import config
from sqlighter import SQLighter
from telebot import types
from datetime import datetime

NEWS_LIMIT = 10
keyword = ''
start_position = 0

bot = telebot.TeleBot(config.TOKEN, parse_mode='HTML')
db = SQLighter('../db/news.sqlite')

def getMainMenu():
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup.add('/news', types.KeyboardButton("Не нажимать!"))
    return start_markup

def getNewsMenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/next10', '/news')
    return markup

@bot.message_handler(commands=['next10'])
def next10(message):
    send_news_next(message)


@bot.message_handler(commands=['start'])
def command_start(message):
    #start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #start_markup.add('/news')
    bot.send_message(message.chat.id, "Hello", reply_markup=getMainMenu())


@bot.message_handler(commands=['news'])
def command_news(message):
    global start_position
    global keyword
    start_position = 0
    keyword = ""
    sent = bot.send_message(message.chat.id, "Enter keyword")
    bot.register_next_step_handler(sent, send_news)

def send_news(message):
    global keyword
    keyword = message.text.strip()
    news = get_news(keyword, NEWS_LIMIT, start_position)
    #start_position = start_position + NEWS_LIMIT
    bot.send_message(message.chat.id, news, reply_markup=getNewsMenu())

def send_news_next(message):
    #keyword = message.text.strip()
    global keyword
    global start_position
    start_position = start_position + NEWS_LIMIT
    news = get_news(keyword, NEWS_LIMIT, start_position)
    #start_position = start_position + NEWS_LIMIT
    bot.send_message(message.chat.id, news, reply_markup=getNewsMenu())


def get_news(keyword, limit, start_position):
    news = db.get_news(keyword, limit, start_position).fetchall()
    strNews = f'<b>{keyword}</b>\n-------------------------\n'
    for snews in news:
        strNews+= datetime.utcfromtimestamp(int(snews[3])/1000).strftime('%d.%m.%Y %H:%M') + f" ({snews[5]})" +'\n'
        strNews+= snews[1] + '\n\n'
    strNews = strNews.replace('&nbsp;', ' ')
    return strNews










@bot.message_handler(content_types='text')
def text_input(message):
    bot.send_message(message.chat.id, f"Дорогой {message.from_user.first_name}, я же просил не нажимать!!!")

bot.infinity_polling()
