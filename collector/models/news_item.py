from pydantic import BaseModel
from datetime import datetime


class NewsItem(BaseModel):
    url: str
    date: datetime
    news: str
    links: str
    agency: str
    title: str = ""
    resume: str = ""
    embedding: list[float] = []
    category: str = ""
