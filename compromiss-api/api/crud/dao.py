from api.crud.schemas import UpdateNewsItem
from api.news.models import NewsView
from api.dao.base import BaseDao
from sqlalchemy import and_, insert, delete, update
from api.db import asmi_async_session_maker

from typing import Any


class CrudDao(BaseDao):
    """News DAO - Data Access Object to News"""
    model = NewsView

    @staticmethod
    async def insert_news_batch(news_items: list[dict[str, Any]]) -> int:
        """
        Асинхронно вставляет пакет новостей в базу данных.

        :param news_items: Список словарей, каждый из которых представляет новость
        :return: Количество успешно вставленных записей
        """
        async with asmi_async_session_maker() as session:
            try:
                result = await session.execute(
                    insert(NewsView),
                    news_items
                )
                await session.commit()
                inserted_count = len(news_items)
                return inserted_count
            except Exception as e:
                await session.rollback()
                raise e

    @staticmethod
    async def delete_news_batch(condition: dict[str, Any]) -> int:
        """
        Асинхронно удаляет набор новостей из базы данных по заданному условию.

        :param condition: Словарь с условиями для удаления
        :return: Количество удаленных записей
        """
        async with asmi_async_session_maker() as session:
            try:
                query = delete(NewsView)
                filters = []
                for k, v in condition.items():
                    if isinstance(v, list):
                        filters.append(getattr(NewsView, k).in_(v))
                    else:
                        filters.append(getattr(NewsView, k) == v)
                if filters:
                    query = query.where(and_(*filters))
                result = await session.execute(query)
                await session.commit()
                return result.rowcount
            except Exception as e:
                await session.rollback()
                raise e

    @staticmethod
    async def update_news_batch(updates: list[UpdateNewsItem]) -> int:
        """
        Асинхронно обновляет набор новостей в базе данных.

        :param updates: Список объектов UpdateNewsItem с url и новым embedding для каждой новости
        :return: Количество обновленных записей
        """
        async with asmi_async_session_maker() as session:
            try:
                updated_count = 0
                for item in updates:
                    stmt = (
                        update(NewsView)
                        .where(NewsView.url == item.url)
                        .values(embedding=item.embedding)
                    )
                    result = await session.execute(stmt)
                    updated_count += result.rowcount
                await session.commit()
                return updated_count
            except Exception as e:
                await session.rollback()
                raise e
