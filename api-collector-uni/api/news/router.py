from fastapi import APIRouter, Query, Depends

from api.news.time_manager import NewsTimeManager, ServiceMode
from api.news.dao import NewsDao
from api.news.schemas import BackendViewSchema, ServiceModeEnum
from api.models.services import get_universal_model


import pandas as pd
from datetime import datetime

router = APIRouter(
    prefix='/news',
    tags=['News'],
)


@router.get('/get/{start_date}/{end_date}')
async def fetch_dates_news(start_date: datetime, end_date: datetime) -> list[BackendViewSchema]:
    """Handler to fetch past news over a period of time"""
    return await NewsDao.get_news_by_date(start=start_date, end=end_date)


@router.get("/get/user_df")
async def get_user_df(
        service_mode: ServiceModeEnum,
        start_date: datetime | None = Query(default=None),
        end_date: datetime | None = Query(default=None)
) -> list[BackendViewSchema]:
    """
    Получает DataFrame с новостями на основе указанных параметров.
    Retrieves a DataFrame with news based on the specified parameters.

    :param service_mode: Режим работы сервиса | Service operation mode
    :param start_date: Начальная дата (опционально) | Start date (optional)
    :param end_date: Конечная дата (опционально) | End date (optional)
    :return: DataFrame с новостями | DataFrame with news
    """
    time_manager = NewsTimeManager(ServiceMode[service_mode.upper()], start_date, end_date)
    start_time, end_time = time_manager.get_time_range()

    news_list = await NewsDao.get_news_by_date(start=start_time, end=end_time)

    news_df = pd.DataFrame(news_list)
    news_records = news_df.to_dict(orient='records')
    return [BackendViewSchema(**record) for record in news_records]


@router.get('/find_similar')
async def find_similar_news(query: str, limit: int = 100, universalizer=Depends(get_universal_model)) -> list[BackendViewSchema]:
    """Handler to fetch most simular news to transferable query over a period of time"""
    embedding = (await universalizer.get_embeddings(texts=[query]))[0]
    return await NewsDao.search_similar_embeddings(embedding=embedding, limit=limit)
