from pydantic import BaseModel, Field

class News(BaseModel):
    title: str
    url: str
    date: str
    negative: float
    neutral: float
    positive: float