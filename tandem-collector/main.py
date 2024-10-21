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

    async with NewsAPIClient() as api_client:
        parser = NewsParser(api_client)
        processor = NewsProcessor(parser)
        fresh_news = await processor.process_agencies(agencies_dict)

    async with DatabaseManager() as db_manager:
        total_count = await db_manager.insert_news_items(fresh_news)

    if not fresh_news:
        logger.warning('Не было получено новостей')
    else:
        end_date = datetime.now()
        total_seconds = (end_date - start_date).total_seconds()
        minutes, seconds = divmod(total_seconds, 60)
        logger.info(f'Время выполнения {int(minutes)} минут и {int(seconds)} секунд')
        # logger.info(f'Execution time: {(seconds / 60):.2f}  minutes')
        logger.info(f'Средняя скорость обработки одной новости: {(total_seconds / total_count):.2f} секунд')



def main():
    """
    Главная функция для запуска процесса сбора новостей по расписанию.
    Main function to start the news collection process on schedule.
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(process_news, 'cron', minute=0)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    asyncio.run(process_news())
    asyncio.set_event_loop(asyncio.new_event_loop())
    # main()
