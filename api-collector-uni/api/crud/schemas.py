from pydantic import BaseModel
from datetime import datetime
from typing import Any


class NewsViewSchema(BaseModel):
    url: str
    title: str
    resume: str
    news: str
    date: datetime
    agency: str
    category: str
    links: list[str] | None
    embedding: list[float] | None

    class Config:
        from_orm = True


class NewsItemBatchSchema(BaseModel):
    items: list[NewsViewSchema]


class DeleteCondition(BaseModel):
    condition: dict[str, Any]


class UpdateNewsItem(BaseModel):
    url: str
    embedding: list[float]


class UpdateNewsBatchSchema(BaseModel):
    updates: list[UpdateNewsItem]
