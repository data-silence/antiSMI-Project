from fastapi import APIRouter, Depends

from api.models.services import get_classifier_model, get_embedding_model, get_headline_model, get_summary_model

router = APIRouter(
    prefix='/models',
    tags=['Models'],
)


@router.post('/generate_embs')
async def make_emb(query: list[str], embedder=Depends(get_embedding_model)) -> list[list[float]]:
    """Handler to fetch most simular news to transferable query over a period of time"""
    return await embedder.get_embeddings(texts=query)


@router.post('/get_category')
async def get_category(text: list[str], categorizer=Depends(get_classifier_model)) -> list[str]:
    return await categorizer.predict_categories(text)


@router.post("/generate_headlines")
async def generate_headline_endpoint(article_texts: list[str], headliner=Depends(get_headline_model)) -> list[str]:
    """
    Асинхронный эндпоинт для генерации заголовков для списка новостей.
    """
    return await headliner.process(article_texts)


@router.post("/generate_resumes")
async def generate_resume_endpoint(article_texts: list[str], summarizer=Depends(get_summary_model)) -> list[str]:
    """
    Асинхронный эндпоинт для генерации заголовков для списка новостей.
    """
    return await summarizer.process(article_texts)
