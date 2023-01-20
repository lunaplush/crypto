from pydantic import BaseModel

class News(BaseModel):
    title: str
    url: str
    date: str