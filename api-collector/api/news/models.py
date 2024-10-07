from sqlalchemy import String, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import mapped_column, Mapped, relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime

from api.db import Base


# Модель для представления news_view
class NewsView(Base):
    __tablename__ = 'news_view'

    url: Mapped[str] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    resume: Mapped[str] = mapped_column(nullable=False)
    news: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(primary_key=True)
    links: Mapped[list[str]] = mapped_column(ARRAY(String))
    agency: Mapped[str] = mapped_column(nullable=False)
    embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=False)


# Модель для представления backend_view
class BackendView(Base):
    __tablename__ = 'backend_view'

    url: Mapped[str] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    resume: Mapped[str] = mapped_column(nullable=False)
    news: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(primary_key=True)
    links: Mapped[list[str]] = mapped_column(ARRAY(String))
    agency: Mapped[str] = mapped_column(nullable=False)
    embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=False)
    media_type: Mapped[str] = mapped_column(nullable=False)


# Модель для таблицы News
class News(Base):
    __tablename__ = 'news'

    url: Mapped[str] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(primary_key=True, nullable=False)

    title: Mapped[str] = mapped_column(nullable=False)
    resume: Mapped[str] = mapped_column(nullable=False)
    news: Mapped[str] = mapped_column(nullable=False)
    links: Mapped[list[str]] = mapped_column(ARRAY(String))
    agency_id: Mapped[str] = mapped_column(ForeignKey('agencies.id'), nullable=False)
    category_id: Mapped[str] = mapped_column(ForeignKey('categories.id'), nullable=False)

    agency: Mapped["Agencies"] = relationship(back_populates='news_items')
    category: Mapped["Categories"] = relationship(back_populates='news_items')
    embeddings: Mapped["Embs"] = relationship("Embs", back_populates='news')


class Embs(Base):
    __tablename__ = 'embs'

    url: Mapped[str] = mapped_column(ForeignKey("view.url"), primary_key=True)
    date: Mapped[DateTime] = mapped_column(ForeignKey("news.date"), primary_key=True)
    embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=False)

    news = relationship("News", back_populates='embeddings')


class Agencies(Base):
    __tablename__ = 'agencies'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    telegram: Mapped[str] = mapped_column()
    is_parsing: Mapped[bool] = mapped_column()
    priority: Mapped[str] = mapped_column()
    mono_category: Mapped[str] = mapped_column()
    ya_link: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    zip_code: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    region: Mapped[str] = mapped_column()
    rf_feds_subj: Mapped[str] = mapped_column()
    settlement_type: Mapped[str] = mapped_column()
    settlement_name: Mapped[str] = mapped_column()
    phone: Mapped[str] = mapped_column()
    chief_name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    last: Mapped[str] = mapped_column()
    first: Mapped[str] = mapped_column()
    middle: Mapped[str] = mapped_column()
    street: Mapped[str] = mapped_column()
    street_type: Mapped[str] = mapped_column()
    language: Mapped[str] = mapped_column()
    prior_country: Mapped[str] = mapped_column()
    benef_country: Mapped[str] = mapped_column()
    is_forbidden: Mapped[bool] = mapped_column(nullable=False)
    media_type: Mapped[str] = mapped_column()

    news_items = relationship('News', back_populates='agency')


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    russian_title: Mapped[str] = mapped_column(nullable=False)
    emoji: Mapped[str] = mapped_column(nullable=False)

    news_items = relationship('News', back_populates='category')
