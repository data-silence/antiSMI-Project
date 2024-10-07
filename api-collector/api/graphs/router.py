from datetime import datetime

from fastapi import APIRouter, HTTPException

from wordcloud import WordCloud
import io
from fastapi.responses import Response

from api.news.dao import NewsDao
from api.graphs.services import normalize_row
import pandas as pd

router = APIRouter(
    prefix='/graphs',
    tags=['Graphs'],
)


@router.get("/wordcloud")
async def get_wordcloud(start_date: datetime, end_date: datetime):
    try:
        # Получаем данные из базы данных
        news_data = await NewsDao.get_news_by_date(start=start_date, end=end_date)

        # Преобразуем данные в pandas DataFrame и выбираем только заголовки
        df = pd.DataFrame(news_data)
        df['normalized_title'] = df['title'].apply(normalize_row)
        titles = " ".join(df['normalized_title'].astype(str))
        unique_words = set(titles.split())
        unique_titles = " ".join(unique_words)

        # Генерируем облако слов
        wordcloud = WordCloud(
            background_color="black", width=1200, height=600, collocations=False
        ).generate(unique_titles)

        # Сохраняем изображение в байтовый поток
        img_byte_arr = io.BytesIO()
        wordcloud.to_image().save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return Response(content=img_byte_arr.getvalue(), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
