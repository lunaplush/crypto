import sys
sys.path.append("..")
from datetime import datetime
from fastapi import FastAPI, Request, Response, status
import uvicorn

import config
from app import sqlighter

from schemas import news
from app import news as newsapp

app = FastAPI()

db = sqlighter.SQLighter(config.PATH_TO_DB)

@app.get("/")
def test():
    return "hello from FastAPI"


@app.get("/news", response_model=list[news.News], status_code=status.HTTP_200_OK)
def get_news(keyword: str = "", start_position: int = 0, limit: int = config.NEWS_LIMIT_PER_PAGE) -> list:
    dataNews = newsapp.News.getNewsByKeyword(db=db, keyword=keyword, start_position=start_position, limit=limit)
    #print(dataNews)
    list_news = []
    for snews in dataNews:
        #list_news.append({"title" : snews['title'], "date" : datetime.utcfromtimestamp(int(snews["date"])/1000).strftime('%d.%m.%Y %H:%M')})
        list_news.append(
            {
                "title" : snews['title'],
                "url" : snews['url'],
                #"date" : datetime.utcfromtimestamp(int(snews["date"])/1000).strftime('%d.%m.%Y %H:%M')
                "date" : snews['date']
            }
        )
    
    return list_news
        
    


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)