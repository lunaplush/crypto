import sys
sys.path.append("..")
from datetime import datetime
from fastapi import FastAPI, Request, Response, status, Query
import uvicorn

from app import dateconterter as dc

import config
from app import sqlighter

import schemas
from app import news as newsapp

app = FastAPI()

db = sqlighter.SQLighter(config.PATH_TO_DB)

@app.get("/")
def test():

    dd = dc.getDates("-7d", type="")
    print(dd)
    dt = dc.strToDatetime("01.01.2023")
    ts = dc.datetimeToTimestamp(dt)
    #return f"hello from FastAPI  / {objDt}"
    return f"""
        {dt} : {ts}
    """


@app.get("/news", response_model=list[schemas.News], status_code=status.HTTP_200_OK, description="get news from db")
async def get_news( keyword: str = Query(default="", max_length=30, description="Search keyword"), 
                    date_start: int = Query(default=None, example="1672520400000"),
                    date_end: int = Query(default=None, example="1672521400000"),
                    start_position: int = 0,
                    limit: int = config.NEWS_LIMIT_PER_PAGE ) -> list:
    try:
        dataNews = newsapp.News.getNewsByKeyword(db=db, keyword=keyword, dateStart=date_start, dateEnd=date_end, start_position=start_position, limit=limit)
        #print(dataNews)
        list_news = []
        for snews in dataNews:
            #list_news.append({"title" : snews['title'], "date" : datetime.utcfromtimestamp(int(snews["date"])/1000).strftime('%d.%m.%Y %H:%M')})
            list_news.append(
                {
                    "title" : snews['title'],
                    "url" : snews['url'],
                    "date" : snews['date'],
                    "negative" : snews['negative'],
                    "neutral" : snews['neutral'],
                    "positive" : snews['positive']
                }
            )
        
        return list_news
    except ValueError as e:
        print(e)
    


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)