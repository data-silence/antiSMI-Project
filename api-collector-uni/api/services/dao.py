from api.news.models import News, Embs, Agencies, Categories, NewsView
from api.dao.base import BaseDao
from api.db import asmi_async_session_maker

from sqlalchemy import select


class ServicesDao(BaseDao):
    model = NewsView

    @staticmethod
    async def get_missing_embs(**filter_by):
        """Picks up news between two daytime values using filter"""
        async with asmi_async_session_maker() as session:
            query = (
                select(
                    News.url,
                    News.date,
                    Embs.embedding,
                    Agencies.telegram,
                    Categories.category
                )
                .outerjoin(Embs, News.url == Embs.url)
                .join(Agencies, News.agency_id == Agencies.id)
                .join(Categories, News.category_id == Categories.id)
                .where(Embs.embedding == None)
            )
            result = await session.execute(query)
            return result.mappings().all()
