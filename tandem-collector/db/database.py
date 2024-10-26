import asyncpg
import json
from datetime import datetime
from loguru import logger
import os
from typing import Union

# from dotenv import load_dotenv
# load_dotenv()

from models.news_item import NewsItem, OldNewsItem


class DatabaseManager:
    def __init__(self):
        # Конфигурация для основной базы данных
        self.main_db_config = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS")
        }
        # Конфигурация для старой базы данных
        self.old_db_config = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "database": os.getenv("OLD_DB_NAME"),  # Новая переменная окружения
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS")
        }
        self.main_pool = None
        self.old_pool = None

    async def __aenter__(self):
        # Создаем пулы подключений для обеих баз данных
        self.main_pool = await asyncpg.create_pool(**self.main_db_config)
        self.old_pool = await asyncpg.create_pool(**self.old_db_config)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Закрываем оба пула при выходе из контекстного менеджера
        await self.main_pool.close()
        await self.old_pool.close()

    async def get_last_agencies_dict(self) -> dict[str, int]:
        """
        Получает словарь с последними id новостей для каждого агентства.
        """
        async with self.main_pool.acquire() as conn:
            query = """
            SELECT t1.agency, 
                   COALESCE(SPLIT_PART(n.url, '/', -1), '0') AS last_news_id
            FROM
                (SELECT a.telegram AS agency, MAX(n.date) AS date
                 FROM agencies a
                 LEFT JOIN news n ON a.id = n.agency_id
                 WHERE a.is_parsing is True
                 GROUP BY a.telegram) t1
            LEFT JOIN news n ON n.date = t1.date AND n.agency_id = (SELECT id FROM agencies WHERE telegram = t1.agency)
            """
            result = await conn.fetch(query)
            return {agency: int(last_url_number) for agency, last_url_number in result}

    @staticmethod
    def ensure_naive_datetime(dt: datetime) -> datetime:
        """Убеждается, что datetime не имеет информации о часовом поясе."""
        return dt.replace(tzinfo=None) if dt.tzinfo else dt

    @staticmethod
    def prepare_embedding(embedding: list[float]) -> str:
        """Преобразует список с embedding в строку JSON."""
        return json.dumps(embedding)

    async def insert_or_update_news_item(
            self,
            conn,
            item: Union[NewsItem, OldNewsItem],
            is_old_format: bool = False
    ) -> bool:
        """
        Вставляет или обновляет одну новость.

        Args:
            conn: Соединение с базой данных
            item: Объект новости (NewsItem или OldNewsItem)
            is_old_format: Флаг, указывающий на формат новости
        """
        processed_dt = self.ensure_naive_datetime(item.date)

        try:
            if is_old_format:
                # SQL для старой базы данных
                await conn.execute('''
                    INSERT INTO news (url, date, news, links, agency, title, resume, category)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                ''', item.url, processed_dt, item.news, item.links,
                                   item.agency, item.title, item.resume, item.category)
            else:
                # SQL для новой базы данных
                processed_embedding = self.prepare_embedding(item.embedding)
                await conn.execute('''
                    INSERT INTO news_view (url, date, news, links, agency, title, resume, embedding, category)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ''', item.url, processed_dt, item.news, item.links,
                                   item.agency, item.title, item.resume, processed_embedding, item.category)
            return True
        except Exception as e:
            logger.error(f"Ошибка при вставке/обновлении новости с URL {item.url}: {str(e)}")
            return False

    async def insert_news_items(self, news_items: dict[str, list[NewsItem]]) -> int:
        """Вставляет или обновляет набор новостей в основную базу данных."""
        if not news_items or all(len(items) == 0 for items in news_items.values()):
            logger.warning("Не поступило новостей для вставки.")
            return 0

        total_count = sum(len(items) for items in news_items.values())
        success_count = 0
        fail_count = 0

        async with self.main_pool.acquire() as conn:
            for items in news_items.values():
                for item in items:
                    if await self.insert_or_update_news_item(conn, item):
                        success_count += 1
                    else:
                        fail_count += 1

        logger.info(f"Всего поступило новостей: {total_count}")
        logger.info(f"Успешно вставлено/обновлено: {success_count}")
        logger.info(f"Не удалось вставить/обновить: {fail_count}")
        return total_count

    async def insert_old_news_items(self, news_items: dict[str, list[OldNewsItem]]) -> int:
        """Вставляет или обновляет набор новостей в старую базу данных."""
        if not news_items or all(len(items) == 0 for items in news_items.values()):
            logger.warning("Не поступило новостей старого формата для вставки.")
            return 0

        total_count = sum(len(items) for items in news_items.values())
        success_count = 0
        fail_count = 0

        async with self.old_pool.acquire() as conn:
            for items in news_items.values():
                for item in items:
                    if await self.insert_or_update_news_item(conn, item, is_old_format=True):
                        success_count += 1
                    else:
                        fail_count += 1

        logger.info(f"Всего поступило новостей старого формата: {total_count}")
        logger.info(f"Успешно вставлено/обновлено: {success_count}")
        logger.info(f"Не удалось вставить/обновить: {fail_count}")
        return total_count