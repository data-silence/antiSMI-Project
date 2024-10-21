from pydantic import BaseModel
from pydantic_core import Url
from enum import Enum

from datetime import datetime


class BackendViewSchema(BaseModel):
    url: Url
    title: str
    resume: str
    news: str
    date: datetime
    agency: str
    category: str
    links: list[Url] | None
    embedding: list[float] | None
    media_type: str

    class Config:
        from_attributes = True


class NewsSchema(BaseModel):
    url: Url
    title: str
    resume: str
    news: str
    date: datetime
    agency: str
    category: str
    links: list[Url] | None
    embedding: list[float] | None

class ServiceModeEnum(str, Enum):
    WHOLE = 'whole'
    LAST24 = 'last24'
    PRECISION = 'precision'
    DIGEST = 'digest'
