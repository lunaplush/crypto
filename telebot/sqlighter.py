import sqlite3
from crypto_news_lib import get_sentiment

class SQLighter:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_news(self, keyword="", limit=1, start_position = 0, status=True):
        if(keyword == ""):
            sql = "SELECT * FROM news ORDER BY date LIMIT 0, 10"
        else:
            sql = f"SELECT * FROM news WHERE title LIKE ('%{keyword}%') ORDER BY date DESC LIMIT {start_position}, {limit}"
        
        with self.connection:
            # ТУТ нужно оценить настроение новости
            #for n in news:
            #    get_sentiment(n)
            result = self.cursor.execute(sql)
            print(result)
            return result

    def close(self):
        self.connection.close()