import aiohttp
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional

from models.news_item import NewsItem
from api.client import NewsAPIClient

class NewsParser:
    def __init__(self, api_client: NewsAPIClient):
        self.api_client = api_client

    @staticmethod
    async def fetch(session: aiohttp.ClientSession, url: str) -> str:
        """
        Получает HTML-контент по указанному URL.
        Fetches HTML content from the specified URL.
        """
        async with session.get(url) as response:
            return await response.text()

    @staticmethod
    def extract_link(tag_a: Optional[BeautifulSoup], url: str) -> str:
        """
        Извлекает ссылку из HTML-тега или возвращает исходный URL.
        Extracts link from HTML tag or returns the original URL.
        """
        if not tag_a:
            return url
        href = tag_a.get('href')
        if href.startswith(('tg://resolve?domain=', 'https://t.me/+')):
            return url
        links = href.split('?utm')[0]
        links = links.split('?')[0] if not links.startswith('https://www.youtube.com/watch') else links
        return links if links and links != '' else url

    async def process_news_content(self, news_content: BeautifulSoup, agency: str) -> Optional[NewsItem]:
        """
        Обрабатывает содержимое новости и создает объект NewsItem.
        Processes news content and creates a NewsItem object.
        """
        dirty_news = news_content.find(attrs={'class': 'tgme_widget_message_text js-message_text'})
        if not dirty_news:
            return None

        url = news_content.find(attrs={'class': 'tgme_widget_message_date'}).get('href')
        date = datetime.fromisoformat(news_content.find(attrs={'class': 'time'}).get('datetime'))
        tag_a = dirty_news.find('a')
        links = self.extract_link(tag_a, url)

        news = dirty_news.text
        if agency == 'briefsmi':
            news = news.split(': ')[-1].split('#')[0]

        news = await self.api_client.clean_text(news, agency)

        return NewsItem(
            url=url,
            date=date,
            news=news,
            links=links,
            agency=agency
        )

    async def parse_agency(self, agency: str, last_id: int) -> list[NewsItem]:
        """
        Парсит новости для конкретного агентства.
        Parses news for a specific agency.
        """
        agency_url = f'https://t.me/s/{agency}'
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, agency_url)
            soup = BeautifulSoup(html, 'lxml')
            news_pages = soup.body.main.section.find_all(attrs={'class': 'tgme_widget_message_bubble'})
            last_news_pages = [page for page in news_pages if int(
                page.find(attrs={'class': 'tgme_widget_message_date'}).get('href').split('/')[-1]) > last_id]

            tasks = [self.process_news_content(news_content, agency) for news_content in last_news_pages]
            return [item for item in await asyncio.gather(*tasks) if item]