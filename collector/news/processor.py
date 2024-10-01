import asyncio
from loguru import logger

from models.news_item import NewsItem
from news.parser import NewsParser
from api.client import NewsAPIClient
import pickle


class NewsProcessor:
    def __init__(self, parser: NewsParser, api_client: NewsAPIClient):
        self.parser = parser
        self.api_client = api_client

    async def process_agencies(self, agencies: dict[str, int]) -> dict[str, list[NewsItem]]:
        """
        Обрабатывает новости для всех агентств.
        Processes news for all agencies.
        """
        all_news = {}
        for agency, last_id in agencies.items():
            logger.info(f'Начинается обработка {agency}')
            # logger.info(f'Starting processing for {agency}')
            news_items = await self.parser.parse_agency(agency, last_id)
            if news_items:
                all_news[agency] = news_items
                await self.enrich_news_items(news_items)

        return all_news

    async def enrich_news_items(self, news_items: list[NewsItem]):
        """
        Обогащает новостные элементы дополнительной информацией.
        Enriches news items with additional information.
        """
        texts = [item.news for item in news_items]

        embeddings_task = self.api_client.generate_embs(texts)
        categories_task = self.api_client.get_category(texts)
        resumes_task = self.api_client.generate_resumes(texts)
        headlines_task = self.api_client.generate_headlines(texts)

        embeddings, categories, resumes, headlines = await asyncio.gather(
            embeddings_task, categories_task, resumes_task, headlines_task
        )

        for i, item in enumerate(news_items):
            item.embedding = embeddings[i]
            item.category = categories[i]
            item.resume = resumes[i]
            item.title = headlines[i]

        logger.info(f'Собрано {len(news_items)} новостей')
        # logger.info(f'Collected {len(news_items)} news items')
        return news_items
