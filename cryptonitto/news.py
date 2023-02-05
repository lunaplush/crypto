import pandas as pd
import numpy as np
import ast
from datetime import timedelta
from cryptonitto import fastapi


def get_from_file(file_path):
    """
    Функция возвращает DataFrame с данными из репозитория с csv
    :param file_path: путь к файлу
    :return:
    """
    df = pd.read_csv(file_path, dtype={"number": np.intc, "negative": np.intc,
                                "positive": np.intc, "negative": np.intc},
                      parse_dates=["Date"]
                     )
    return df


def get_integral_news_info(symbol, date_work, keywords, day_number=3):
    """
    Функция возваращает интегральную характеристику настроеня новостей для одной даты
    :param symbol: идентификатор криптовалют соотвествует именм  в yahoo finance
    :param date_work: дата, для которой считается оценка новостей
    :param keywords: ключевые словая, по которым выбираются новости из базы данных
    :param day_number: количество дней, по которым скачиваются новости для интегрального оценивания
    :return: pandas.Series ("negative", "positive", "neutral", "number" )
    """

    date_begin = int((date_work.replace(hour=0, minute=0, second=0)-timedelta(days=day_number-1)).timestamp() * 1000)
    date_end = int((date_work.replace(hour=23, minute=59, second=59).timestamp() * 1000))

    news_list = []
    for keyword in keywords:
        response = fastapi.git_list_news(keyword, date_begin, date_end)
        news_list += ast.literal_eval(response.content.decode(encoding=response.apparent_encoding))
    print(f"--{symbol} --- Found {len(news_list)} news for {date_work}--")

    if len(news_list) > 0:
        sentiment = News.getNewsSentiment(news_list)

        line = pd.Series(name=date_work.replace(hour=0, minute=0, second=0, microsecond=0),
                         data={"number": len(news_list), "negative": sentiment["negative"],
                               "neutral": sentiment["neutral"],
                               "positive": sentiment["positive"]}
                         )
        return line
    else:
        return None

def get_news_for_day(symbol, date_work, keywords, day_number = 3):
    date_begin = int((date_work.replace(hour=0, minute=0, second=0)-timedelta(days=day_number-1)).timestamp() * 1000)
    date_end = int((date_work.replace(hour=23, minute=59, second=59).timestamp() * 1000))

    news_list = []
    for keyword in keywords:
        responce = fastapi.git_list_news(keyword,date_begin, date_end)
        news_list += ast.literal_eval(responce.content.decode(encoding=responce.apparent_encoding))
    return news_list


class News:
    def __init__(self) -> None:
        pass

    def getNewsByKeyword(db, keyword="", dateStart=None, dateEnd=None, limit=None, start_position=0, status=True):
        if limit is None:
            sql_limit = ""
        else:
            sql_limit = f" LIMIT {start_position}, {limit}"
        
        if dateStart is not None and dateEnd is not None:
            sql_where_date = f"date>={dateStart} AND date<={dateEnd}"
        elif dateStart is not None and dateEnd is None:
            sql_where_date = f"date>={dateStart}"
        elif dateStart is None and dateEnd is not None:
            sql_where_date = f"date<={dateEnd}"
        else:
            sql_where_date = ""


        if(keyword == ""):
            if sql_where_date == "":
                sql = f"SELECT * FROM news ORDER BY date {sql_limit}"
            else:
                sql = f"SELECT * FROM news WHERE {sql_where_date} ORDER BY date {sql_limit}"
        else:
            if sql_where_date == "":
                #sql = f"SELECT * FROM news WHERE title LIKE ('%{keyword}%') ORDER BY date DESC LIMIT {start_position}, {limit}"
                sql = f"SELECT title, date, negative, neutral, positive FROM news AS n INNER JOIN tf_idf AS t ON n.url=t.url WHERE title LIKE ('%{keyword} %') OR title LIKE (' %{keyword} %') OR title LIKE (' %{keyword}%') GROUP BY title ORDER BY date DESC {sql_limit}"
            else:
                sql = f"SELECT title, date, negative, neutral, positive FROM news AS n INNER JOIN tf_idf AS t ON n.url=t.url WHERE (title LIKE ('%{keyword} %') OR title LIKE (' %{keyword} %') OR title LIKE (' %{keyword}%')) AND {sql_where_date} GROUP BY title ORDER BY date DESC {sql_limit}"
        print(sql)
        return db.query(sql).fetchall()



    def getNewsSentiment(news):
        data = []
        for snews in news:
            #print(snews['title'])
            #print(f"Negative: {snews['negative']} / Neutral: {snews['neutral']} / Positive: {snews['positive']}")
            sentiment = News.getSingleNewsSentiment(snews)
            #print(sentiment)
            data.append(sentiment)
        
        dictionary = {
            'negative': 0,
            'neutral': 0,
            'positive': 0
        }
        for item in data:
            dictionary[item] += 1

        sum = dictionary['negative'] + dictionary['neutral'] + dictionary['positive']
        # Считаем, сколько процентов позитивных и негатевных новостей
        if(sum != 0):
            dictionary["positive"] =  int(round((100 / sum) * dictionary["positive"], 0))
            dictionary["negative"] = int(round((100 / sum) * dictionary["negative"], 0))
            dictionary["neutral"] = 100 - dictionary["positive"] - dictionary["negative"]
        return dictionary


    def getSingleNewsSentiment(newsData):
        negative, neutral, positive = float(newsData['negative']), float(newsData['neutral']), float(newsData['positive'])
        #print(type(negative))
        #print(f"Negative: {negative} / Neutral: {neutral} / Positive: {positive}")
        if neutral > 0.5:
            return 'neutral'
        if negative > positive:
            return 'negative'
        else:
            return 'positive'


    def getNewsCount(db, keyword=""):
        if(keyword == ""):
            sql = "SELECT COUNT(*) FROM news"
        else:
            #SELECT COUNT(*) FROM (SELECT title FROM news AS n INNER JOIN tf_idf AS t ON n.url=t.url WHERE title LIKE ('% XMR%') OR title LIKE (' %XMR %') OR title LIKE (' %XRM%') GROUP BY title ORDER BY date DESC)
            sql = f"SELECT COUNT(*) as cnt FROM (SELECT title FROM news AS n INNER JOIN tf_idf AS t ON n.url=t.url WHERE title LIKE ('%{keyword} %') OR title LIKE (' %{keyword} %') OR title LIKE (' %{keyword}%') GROUP BY title ORDER BY date DESC)"

        return db.query(sql).fetchone()['cnt']