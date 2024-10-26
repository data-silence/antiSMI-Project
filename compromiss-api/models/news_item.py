from pydantic import BaseModel
from datetime import datetime


class NewsItem(BaseModel):
    url: str
    date: datetime
    news: str
    links: list = []
    agency: str
    title: str = ""
    resume: str = ""
    embedding: list[float] = []
    category: str = ""
