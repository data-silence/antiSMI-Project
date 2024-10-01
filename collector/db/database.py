import asyncpg
import json
from datetime import datetime
from loguru import logger
import os
# from dotenv import load_dotenv

from models.news_item import NewsItem


# load_dotenv()


class DatabaseManager:
    def __init__(self):
        self.db_config = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS")
        }
        self.pool = None

    async def __aenter__(self):
        self.pool = await asyncpg.create_pool(**self.db_config)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.pool.close()

    async def get_last_agencies_dict(self) -> dict[str, int]:
        """
        Получает словарь с последними новостями для каждого агентства.
        Retrieves a dictionary with the latest news for each agency.
        """
        async with self.pool.acquire() as conn:
            query = """
            SELECT t1.agency, SPLIT_PART(n.url, '/', -1)
            FROM
            (SELECT telegram AS agency, MAX(date) AS date
            FROM news n
            JOIN agencies a ON a.id = n.agency_id
            WHERE date > (SELECT NOW() - INTERVAL '1 month')
            GROUP BY telegram) t1
            JOIN news n 
            ON n.date = t1.date
            """
            result = await conn.fetch(query)
            return {agency: int(last_url_number) for agency, last_url_number in result}

    @staticmethod
    def ensure_naive_datetime(dt: datetime) -> datetime:
        """
        Убеждается, что datetime не имеет информации о часовом поясе.
        Ensures that datetime has no timezone information.
        """
        return dt.replace(tzinfo=None) if dt.tzinfo else dt

    @staticmethod
    def prepare_embedding(embedding: list[float]) -> str:
        """
        Преобразует список с embedding в строку JSON.
        Converts the embedding list to a JSON string.
        """
        return json.dumps(embedding)

    async def insert_or_update_news_item(self, conn, item: NewsItem) -> bool:
        """
        Вставляет или обновляет одну новость.
        Inserts or updates a single news item.
        """
        processed_dt = self.ensure_naive_datetime(item.date)
        processed_embedding = self.prepare_embedding(item.embedding)
        try:
            await conn.execute('''
                INSERT INTO news_view (url, date, news, links, agency, title, resume, embedding, category)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ''', item.url, processed_dt, item.news, item.links,
                               item.agency, item.title, item.resume, processed_embedding, item.category)
            return True
        except Exception as e:
            logger.error(f"Ошибка при вставке/обновлении новости с URL {item.url}: {str(e)}")
            # logger.error(f"Error inserting/updating news with URL {item.url}: {str(e)}")
            return False

    async def insert_news_items(self, news_items: dict[str, list[NewsItem]]):
        """
        Вставляет или обновляет набор новостей.
        Inserts or updates a set of news items.
        """
        total_count = sum(len(items) for items in news_items.values())
        success_count = 0
        fail_count = 0

        async with self.pool.acquire() as conn:
            for items in news_items.values():
                for item in items:
                    if await self.insert_or_update_news_item(conn, item):
                        success_count += 1
                    else:
                        fail_count += 1

        logger.info(f"Всего поступило новостей: {total_count}")
        # logger.info(f"Total news received: {total_count}")
        logger.info(f"Успешно вставлено/обновлено: {success_count}")
        # logger.info(f"Successfully inserted/updated: {success_count}")
        logger.info(f"Не удалось вставить/обновить: {fail_count}")
        # logger.info(f"Failed to insert/update: {fail_count}")
