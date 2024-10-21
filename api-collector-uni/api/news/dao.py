from api.news.models import BackendView, News, Embs, Agencies, Categories
from api.dao.base import BaseDao
from datetime import datetime
from api.db import asmi_async_session_maker

from sqlalchemy import select, and_


class NewsDao(BaseDao):
    """News DAO - Data Access Object to News"""
    model = BackendView

    @staticmethod
    async def get_news_by_date(start: datetime, end: datetime, **filter_by):
        """Picks up news between two daytime values using filter"""
        async with asmi_async_session_maker() as session:
            query = select(BackendView.__table__.columns).where(
                and_(start <= BackendView.date, BackendView.date <= end)
            ).filter_by(**filter_by).order_by(BackendView.date.desc())
            result = await session.execute(query)
            return result.mappings().all()

    @staticmethod
    async def search_similar_embeddings(embedding: list[float], limit: int):
        """Returns the news that is closest to the embedding that was transferred"""
        async with asmi_async_session_maker() as session:
            # Create the CTE
            cte = (
                select(Embs.url, Embs.date, Embs.embedding)
                .order_by(Embs.embedding.cosine_distance(embedding))
                .limit(limit)
                .cte('subquery_result')
            )
            # Perform the final query with JOIN
            query = (
                select(
                    News.url,
                    News.date,
                    News.title,
                    News.resume,
                    News.news,
                    News.links,
                    Categories.category.label("category"),  # добавляем category из таблицы Categories
                    Agencies.media_type.label("media_type"),  # добавляем media_type из таблицы Agencies
                    Agencies.telegram.label("agency"),  # добавляем telegram  из таблицы Agencies как agency
                    cte.c.embedding  # добавляем поле embedding из таблицы News
                )
                .join(cte, (News.url == cte.c.url) & (News.date == cte.c.date))
                .join(Agencies, News.agency_id == Agencies.id)
                .join(Categories, News.category_id == Categories.id)
            )
            result = await session.execute(query)
            return result.mappings().all()



    @staticmethod
    async def search_missing_embeddings():
        """Returns the news that is closest to the embedding that was transferred"""
        async with asmi_async_session_maker() as session:

            # Perform the final query with JOIN
            query = (
                select(
                    News.url,
                    News.date,
                    News.resume,
                    News.news,
                    Embs.embedding  # добавляем поле embedding из таблицы News
                )
                .join(Embs, (News.url == Embs.url) & (News.date == Embs.date))
                .where(Embs.embedding == None)

            )
            result = await session.execute(query)
            return result.mappings().all()