import sys
sys.path.append("..")

import sqlite3
from crypto_news_tf_idf_lib import Sentiment




class SQLighter:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def get_news(self, keyword="", limit=1, start_position = 0, status=True):
        if(keyword == ""):
            sql = f"SELECT * FROM news ORDER BY date LIMIT {start_position}, {limit}"
        else:
            #sql = f"SELECT * FROM news WHERE title LIKE ('%{keyword}%') ORDER BY date DESC LIMIT {start_position}, {limit}"
            sql = f"SELECT title, date, negative, neutral, positive FROM news AS n INNER JOIN tf_idf AS t ON n.url=t.url WHERE title LIKE ('%{keyword} %') OR title LIKE (' %{keyword} %') OR title LIKE (' %{keyword}%') GROUP BY title ORDER BY date DESC LIMIT {start_position}, {limit}"
        
        with self.connection:
            # ТУТ нужно оценить настроение новости
            #for n in news:
            #    get_sentiment(n)
            
            result = self.cursor.execute(sql).fetchall()
            #print(result)
            return result



    def getNewsCount(self, keyword=""):
        if(keyword == ""):
            sql = "SELECT COUNT(*) FROM news"
        else:
            #SELECT COUNT(*) FROM (SELECT title FROM news AS n INNER JOIN tf_idf AS t ON n.url=t.url WHERE title LIKE ('% XMR%') OR title LIKE (' %XMR %') OR title LIKE (' %XRM%') GROUP BY title ORDER BY date DESC)
            sql = f"SELECT COUNT(*) as cnt FROM (SELECT title FROM news AS n INNER JOIN tf_idf AS t ON n.url=t.url WHERE title LIKE ('%{keyword} %') OR title LIKE (' %{keyword} %') OR title LIKE (' %{keyword}%') GROUP BY title ORDER BY date DESC)"

        with self.connection:
            result = self.cursor.execute(sql).fetchone()
            #print(result.keys())
            return result['cnt']




    def query(self, sql):      
        with self.connection:
            return self.cursor.execute(sql).fetchall()

    """
    def insertData(self, data):
        try:
            self.cursor.executemany("INSERT OR IGNORE INTO sentiment VALUES(?, ?, ?, ?)", data)
            result = self.connection.commit()
            print(result)
        except Exception as e:
                if hasattr(e, 'message'):
                    print(f"1: {e.message}")
                else:
                    print(f"2: {e}")
    """


    def insertRow(self, sql):
        """
        print(data['url'])
        print(data['negative'])
        print(data['neutral'])
        print(data['positive'])
        """
        try:
            print(sql)
            self.cursor.execute(sql)
            result = self.connection.commit()
            #print(result)
            return result
        except Exception as e:
            if hasattr(e, 'message'):
                print(f"1: {e.message}")
            else:
                print(f"2: {e}")



    def close(self):
        self.connection.close()