import os

import telebot
from telebot import types
from sqlighter import SQLighter
from datetime import datetime, timedelta

import sys
sys.path.append("..")

import config
import dateconterter
import trends

#from time_series_prediction_lib import Forecast
from time_series_prediction_lib import get_forecast, Forecast




NEWS_LIMIT = 10
#keyword = ''
start_position = 0

bot = telebot.TeleBot(config.TOKEN, parse_mode='HTML')
db = SQLighter('../db/news.sqlite')

"""
def getMainMenu():
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup.add('/news', types.KeyboardButton("Не нажимать!"))
    return start_markup
"""




@bot.message_handler(commands=['start'])
def command_start(message):
    #start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #start_markup.add('/news')
    #bot.send_message(message.chat.id, f'Hello {message.chat.username}', reply_markup=getMainMenu())
    bot.send_message(message.chat.id, f'Hello {message.chat.username}')
    asset = bot.send_message(message.chat.id, "Enter asset name (BTC, ETH, XRP)", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(asset, select_action)


@bot.message_handler(commands=['assetmenu'])
def command_start(message):
    bot.send_message(message.chat.id, 'Select action', reply_markup=assetMainMenu())


def select_action(message):
    global asset
    global start_position
    asset = message.text.strip()
    start_position = 0
    bot.send_message(message.chat.id, f'<b>{asset}</b> has been selected', reply_markup=assetMainMenu())


def assetMainMenu():
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup.add('/trends', '/news', '/forcast', '/start')
    return start_markup

"""
@bot.message_handler(commands=['news'])
def command_news(message):
    global start_position
    global keyword
    start_position = 0
    keyword = ""
    sent = bot.send_message(message.chat.id, "Enter keyword")
    bot.register_next_step_handler(sent, send_news)
"""



#news ==============================================

def getNewsMenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/prev10', '/next10', '/lastnews', '/assetmenu')
    return markup

@bot.message_handler(commands=['next10'])
def next10(message):
    send_news_next(message)

@bot.message_handler(commands=['news'])
def command_news(message):
    global start_position
    global asset
    start_position = start_position + NEWS_LIMIT
    news = get_news(asset, NEWS_LIMIT, start_position)
    bot.send_message(message.chat.id, news, reply_markup=getNewsMenu())

def send_news(message):
    global keyword
    keyword = message.text.strip()
    news = get_news(keyword, NEWS_LIMIT, start_position)
    #start_position = start_position + NEWS_LIMIT
    bot.send_message(message.chat.id, news, reply_markup=getNewsMenu())

def send_news_next(message):
    #keyword = message.text.strip()
    global asset
    global start_position
    start_position = start_position + NEWS_LIMIT
    news = get_news(asset, NEWS_LIMIT, start_position)
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



#trends ===========================================
def menuTrendsSelectPeriod():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/7d', '/1m', '/1y', '/allTime', '/start')
    return markup

@bot.message_handler(commands=['trends'])
def command_news(message):
    bot.send_message(message.chat.id, 'Select pediod', reply_markup=menuTrendsSelectPeriod())


@bot.message_handler(commands=['7d'])
def command_news(message):
    global asset
    bot.send_message(message.chat.id, 'Wait a minute...')

    dd = dateconterter.getDates("-7d")
    symbol = asset+"-USD"
    trendImageFilename = f"{symbol.lower()}_{dd['dateStart']}_{dd['dateEnd']}_7d.png"
    if(os.path.isfile('../data/trends/'+trendImageFilename) == False):
        trends.getTrendImage(symbol, dd['dateStart'], dd['dateEnd'], trendImageFilename)
    
    photo = open('../data/trends/'+trendImageFilename, 'rb')
    bot.send_photo(message.chat.id, photo)



@bot.message_handler(commands=['1m'])
def command_news(message):
    global asset
    bot.send_message(message.chat.id, 'Wait a minute...')

    dd = dateconterter.getDates("-1m")
    symbol = asset+"-USD"
    trendImageFilename = f"{symbol.lower()}_{dd['dateStart']}_{dd['dateEnd']}_1m.png"
    if(os.path.isfile('../data/trends/'+trendImageFilename) == False):
        trends.getTrendImage(symbol, dd['dateStart'], dd['dateEnd'], trendImageFilename)
    
    photo = open('../data/trends/'+trendImageFilename, 'rb')
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['1y'])
def command_news(message):
    global asset
    bot.send_message(message.chat.id, 'Wait a minute...')

    dd = dateconterter.getDates("-1y")
    symbol = asset+"-USD"
    trendImageFilename = f"{symbol.lower()}_{dd['dateStart']}_{dd['dateEnd']}_1y.png"
    if(os.path.isfile('../data/trends/'+trendImageFilename) == False):
        trends.getTrendImage(symbol, dd['dateStart'], dd['dateEnd'], trendImageFilename)
    
    photo = open('../data/trends/'+trendImageFilename, 'rb')
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['allTime'])
def command_news(message):
    global asset
    bot.send_message(message.chat.id, 'Wait a minute...')

    dd = {
        'dateStart': '2005-01-01',
        'dateEnd': dateconterter.formatDate(datetime.now())
    }
    symbol = asset+"-USD"
    trendImageFilename = f"{symbol.lower()}_{dd['dateStart']}_{dd['dateEnd']}_alltime.png"
    if(os.path.isfile('../data/trends/'+trendImageFilename) == False):
        trends.getTrendImage(symbol, dd['dateStart'], dd['dateEnd'], trendImageFilename)
    
    photo = open('../data/trends/'+trendImageFilename, 'rb')
    bot.send_photo(message.chat.id, photo)

#forcast ==========================================

def getForcastMenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/wo_news', '/w_news', '/start')
    return markup


@bot.message_handler(commands=['forcast'])
def command_forcast(message):
    global asset
    bot.send_message(message.chat.id, 'Select forcast type', reply_markup=getForcastMenu())


@bot.message_handler(commands=['wo_news'])
def command_news(message):
    global asset
    symbol = asset+"-USD"
    bot.send_message(message.chat.id, 'Wait a minute...')
    forecast = get_forecast(symbol, date=datetime.now())
    if forecast is not None:
        #print(forecast.path_figure)
        photo = open(forecast.path_figure, 'rb')
        bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, 'There is no prediction... Sorry')



@bot.message_handler(content_types='text')
def text_input(message):
    bot.send_message(message.chat.id, f"Дорогой {message.from_user.first_name}, для этой кнопки действие еще не прописано!")

bot.infinity_polling()
