import asyncio
from datetime import datetime
from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from db.database import DatabaseManager
from news.processor import NewsProcessor
from news.parser import NewsParser
from api.client import NewsAPIClient


async def process_news():
    """
    Основная функция для обработки новостей.
    Main function for news processing.
    """
    start_date = datetime.now()

    async with DatabaseManager() as db_manager:
        # Получение свежего словаря новостных агентств
        # Get the latest dictionary of news agencies
        agencies_dict = await db_manager.get_last_agencies_dict()
        logger.info('Получен статус последних новостей в базе данных')
        # logger.info('Retrieved status of latest news in the database')

    api_client = NewsAPIClient()
    parser = NewsParser(api_client)
    processor = NewsProcessor(parser, api_client)
    fresh_news = await processor.process_agencies(agencies_dict)

    async with DatabaseManager() as db_manager:
        await db_manager.insert_news_items(fresh_news)

    end_date = datetime.now()
    logger.info(f'Время выполнения: {round((end_date - start_date).total_seconds() / 60, 2)} минут')
    # logger.info(f'Execution time: {round((end_date - start_date).total_seconds() / 60, 2)} minutes')


def main():
    """
    Главная функция для запуска процесса сбора новостей по расписанию.
    Main function to start the news collection process on schedule.
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(process_news, 'interval', hours=1)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()