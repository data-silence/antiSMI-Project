from fastapi import APIRouter, HTTPException, Body, Query

from api.crud.dao import CrudDao
from api.crud.schemas import NewsViewSchema, NewsItemBatchSchema, DeleteCondition, UpdateNewsBatchSchema
from api.news.models import NewsView

from datetime import datetime

router = APIRouter(
    prefix='/crud',
    tags=['Crud'],
    include_in_schema=False,
)


# Вставка
@router.post("/insert/news")
async def insert_single_news(news_item: NewsViewSchema):
    try:
        inserted_count = await CrudDao.insert_news_batch([news_item.model_dump()])
        return {"message": f"Successfully inserted {inserted_count} item"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insert/news_batch")
async def insert_news_batch(batch: NewsItemBatchSchema):
    try:
        news_items = [item.model_dump() for item in batch.items]
        inserted_count = await CrudDao.insert_news_batch(news_items)
        return {"message": f"Successfully inserted {inserted_count} items"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Удаление
@router.delete("/delete/news/{url}")
async def delete_single_news(url: str):
    try:
        condition = {"url": url}
        deleted_count = await CrudDao.delete_news_batch(condition)
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="News item not found")
        return {"message": f"Successfully deleted news item with URL: {url}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/news")
async def delete_news_batch(condition: DeleteCondition = Body(...)):
    try:
        deleted_count = await CrudDao.delete_news_batch(condition.condition)
        return {"message": f"Successfully deleted {deleted_count} items"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Обновление
@router.put("/update/news")
async def update_single_news(url: str = Query(...), updated_news: dict = Body(...)):
    try:
        condition = {"url": url}
        # Фильтруем только существующие поля
        valid_fields = set(NewsView.__table__.columns.keys())
        filtered_updates = {k: v for k, v in updated_news.items() if k in valid_fields}

        # Преобразуем строку даты в объект datetime
        if 'date' in filtered_updates:
            try:
                filtered_updates['date'] = datetime.fromisoformat(filtered_updates['date'])
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")

        if not filtered_updates:
            raise HTTPException(status_code=400, detail="No valid fields to update")

        updated_count = await CrudDao.update_news_batch(condition, filtered_updates)
        if updated_count == 0:
            raise HTTPException(status_code=404, detail="News item not found")
        return {"message": f"Successfully updated news item with URL: {url}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update/news_batch")
async def update_news_batch(updates: UpdateNewsBatchSchema):
    try:
        updated_count = await CrudDao.update_news_batch(updates.updates)
        return {"message": f"Successfully updated {updated_count} items"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
