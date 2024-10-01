import aiohttp
from typing import Any


class NewsAPIClient:
    def __init__(self, base_url: str = "http://host.docker.internal:8000"):  # http://127.0.0.1:8000
        self.base_url = base_url

    async def fetch_news_without_embeddings(self) -> dict[str, Any]:
        """
        Получает новости без эмбеддингов.
        Fetches news without embeddings.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/services/get_missing_embs") as response:
                return await response.json()

    async def clean_text(self, text: str, agency: str = None) -> str:
        """
        Очищает текст новости.
        Cleans the news text.
        """
        data = {'text': text}
        if agency:
            data['agency'] = agency
        timeout = aiohttp.ClientTimeout(total=36000)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(f"{self.base_url}/services/clean_text", json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('clean_text', text)
                return text

    async def generate_embs(self, news_list: list[str]) -> list[list[float]]:
        """
        Генерирует эмбеддинги для списка новостей.
        Generates embeddings for a list of news.
        """
        timeout = aiohttp.ClientTimeout(total=36000)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(f"{self.base_url}/models/generate_embs", json=news_list) as response:
                return await response.json()

    async def get_category(self, news: list[str]) -> list[str]:
        """
        Получает категории для списка новостей.
        Gets categories for a list of news.
        """
        timeout = aiohttp.ClientTimeout(total=36000)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(f"{self.base_url}/models/get_category", json=news) as response:
                return await response.json()

    async def generate_resumes(self, news: list[str]) -> list[str]:
        """
        Генерирует резюме для списка новостей.
        Generates summaries for a list of news.
        """
        timeout = aiohttp.ClientTimeout(total=36000)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(f"{self.base_url}/models/generate_resumes", json=news) as response:
                result = await response.json()
                return result

    async def generate_headlines(self, news: list[str]) -> list[str]:
        """
        Генерирует заголовки для списка новостей.
        Generates headlines for a list of news.
        """
        timeout = aiohttp.ClientTimeout(total=36000)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(f"{self.base_url}/models/generate_headlines", json=news) as response:
                result = await response.json()
                return result
