import aiohttp
from typing import Any
import os

API_URL = os.getenv("API")


class NewsAPIClient:
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=36000)
        self.session = None


    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()


    async def fetch_news_without_embeddings(self) -> dict[str, Any]:
        """
        Получает новости без эмбеддингов.
        Fetches news without embeddings.
        """
        async with self.session.post(f"{self.base_url}/services/get_missing_embs") as response:
            return await response.json()

    async def clean_text(self, text: str, agency: str = None) -> str:
        """
        Очищает текст новости.
        Cleans the news text.
        """
        data = {'text': text}
        if agency:
            data['agency'] = agency
        async with self.session.post(f"{self.base_url}/services/clean_text", json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result.get('clean_text', text)
            return text

    async def generate_embs(self, news_list: list[str]) -> list[list[float]]:
        """
        Генерирует эмбеддинги для списка новостей.
        Generates embeddings for a list of news.
        """
        async with self.session.post(f"{self.base_url}/models/generate_embs", json=news_list) as response:
            return await response.json()

    async def get_category(self, news: list[str]) -> list[str]:
        """
        Получает категории для списка новостей.
        Gets categories for a list of news.
        """
        async with self.session.post(f"{self.base_url}/models/get_category", json=news) as response:
            return await response.json()

    async def generate_resumes(self, news: list[str]) -> list[str]:
        """
        Генерирует резюме для списка новостей.
        Generates summaries for a list of news.
        """
        async with self.session.post(f"{self.base_url}/models/generate_resumes", json=news) as response:
            result = await response.json()
            return result

    async def generate_headlines(self, news: list[str]) -> list[str]:
        """
        Генерирует заголовки для списка новостей.
        Generates headlines for a list of news.
        """
        async with self.session.post(f"{self.base_url}/models/generate_headlines", json=news) as response:
            result = await response.json()
            return result
