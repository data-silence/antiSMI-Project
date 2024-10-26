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

class OldNewsItem(BaseModel):
    url: str
    date: datetime
    news: str
    links: str
    agency: str
    title: str = ""
    resume: str = ""
    category: str = ""

    @classmethod
    def from_news_item(cls, item: NewsItem, category: str = "") -> 'OldNewsItem':
        return cls(
            url=item.url,
            date=item.date,
            news=item.news,
            links=", ".join(item.links),
            agency=item.agency,
            title=item.title,
            resume=item.resume,
            category=category
        )

