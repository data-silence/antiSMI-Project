import asyncio
from loguru import logger

from models.news_item import NewsItem, OldNewsItem
from news.parser import NewsParser
import fasttext
import warnings

warnings.filterwarnings("ignore")

# from api.client import NewsAPIClient
# import pickle


class NewsProcessor:
    def __init__(self, parser: NewsParser):
        self.parser = parser
        self.cat_model = fasttext.load_model("models/cat_model.ftz")


    def get_old_category(self, news_list: list[str]) -> list[str]:
        return list(map(lambda x: x[0].split('__label__')[-1], self.cat_model.predict(news_list)[0]))

    async def process_agencies(self, agencies: dict[str, int]) -> tuple[
        dict[str, list[NewsItem]], dict[str, list[OldNewsItem]]]:
        """
        Обрабатывает новости для всех агентств в обоих форматах.
        Processes news for all agencies in both formats.
        """
        all_news = {}
        all_old_news = {}

        for i, (agency, last_id) in enumerate(agencies.items()):
            progress = f'[{(i + 1)}/{len(agencies)}]'
            logger.info(f'Начинается обработка {progress} {agency} ...')

            news_items = await self.parser.parse_agency(agency, last_id)
            if not news_items:
                logger.info(f'... новых новостей нет')
                continue

            # Обработка новостей для обоих форматов
            enriched_items = await self.enrich_news_items(news_items)
            all_news[agency] = enriched_items

            # Создание и обогащение старого формата новостей
            old_categories = self.get_old_category([item.news for item in news_items])
            old_news_items = [
                OldNewsItem.from_news_item(item, category=cat)
                for item, cat in zip(enriched_items, old_categories)
            ]
            all_old_news[agency] = old_news_items

            logger.info(f'... получено [{len(news_items)}] новостей')

        total_count = sum(len(items) for items in all_news.values())
        logger.info(f'Собрано {total_count} новостей')

        return all_news, all_old_news

    async def enrich_news_items(self, news_items: list[NewsItem]) -> list[NewsItem]:
        """
        Обогащает новостные элементы дополнительной информацией.
        Enriches news items with additional information.
        """
        texts = [item.news for item in news_items]

        # Последовательная обработка моделями в оптимальном порядке
        embeddings_task = self.parser.api_client.generate_embs(texts)
        categories_task = self.parser.api_client.get_category(texts)

        embeddings, categories = await asyncio.gather(
            embeddings_task, categories_task
        )

        # Получение резюме и заголовков
        resumes = self.parser.api_client.generate_resumes(texts)
        titles = self.parser.api_client.generate_headlines(texts)

        # Обновление всех элементов
        for i, item in enumerate(news_items):
            item.embedding = embeddings[i]
            item.category = categories[i]
            item.resume = resumes[i]
            item.title = titles[i]

        return news_items

