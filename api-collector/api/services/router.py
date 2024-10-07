from fastapi import APIRouter, Request

from api.news.dao import NewsDao
from api.news.schemas import BackendViewSchema, NewsSchema
from api.services.dao import ServicesDao
from api.news.services import TextCleaner

router = APIRouter(
    prefix='/services',
    tags=['Services'],
)


@router.post('/embs_search')
async def news_search_via_emb(embedding: list[float], limit: int = 50) -> list[BackendViewSchema]:
    return await NewsDao.search_similar_embeddings(embedding=embedding, limit=limit)


@router.post('/get_missing_embs')
async def write_missing() -> list[NewsSchema]:
    return await ServicesDao.get_all(embedding=None)
    # return await ServicesDao.get_missing_embs()


@router.post('/clean_text')
async def clean_news_text(request: Request):
    """Handler to clean news text"""
    data = await request.json()
    text = data.get('text')
    agency = data.get('agency')

    cleaner = TextCleaner()
    clean_text = cleaner.clean_news(text) if not agency else cleaner.clean_news(news=text, channel=agency)

    return {"clean_text": clean_text}
