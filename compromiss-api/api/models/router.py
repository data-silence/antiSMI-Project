from fastapi import APIRouter

from api.models.services import headliner, summarizer, categorizer, embedder

router = APIRouter(
    prefix='/models',
    tags=['Models'],
)


@router.post('/generate_embs')
async def make_emb(query: list[str]) -> list[list[float]]:
    """Handler to fetch most simular news to transferable query over a period of time"""
    return await embedder.get_embeddings(texts=query)


@router.post('/get_category')
async def get_category(text: list[str]) -> list[str]:
    return await categorizer.predict_categories(text)


@router.post("/generate_headlines")
async def generate_headline_endpoint(article_texts: list[str]):
    """
    Асинхронный эндпоинт для генерации заголовков для списка новостей.
    """
    return await headliner.process(article_texts)


@router.post("/generate_resumes")
async def generate_resume_endpoint(article_texts: list[str]):
    """
    Асинхронный эндпоинт для генерации заголовков для списка новостей.
    """
    return await summarizer.process(article_texts)
