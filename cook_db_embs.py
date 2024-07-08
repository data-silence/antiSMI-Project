import asyncio
import asyncpg
from datetime import datetime
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/LaBSE')


def make_embs(sents: list[str]) -> list[str]:
    embeddings = model.encode(sents)
    return [str(emb.tolist()) for emb in embeddings]


async def process_news_embeddings(db_config: dict, batch_size: int = 900):
    async def get_last_processed(conn):
        return await conn.fetchrow(
            "SELECT url, date FROM last_processed_news LIMIT 1"
        )

    async def update_last_processed(conn, url, date):
        await conn.execute(
            """
            INSERT INTO last_processed_news (url, date) 
            VALUES ($1, $2) 
            ON CONFLICT (id) DO UPDATE SET url = $1, date = $2
            """,
            url, date
        )

    async def process_batch(conn, last_url, last_date):
        async with conn.transaction():
            # Используем курсор для эффективной пагинации
            batch = await conn.fetch(
                """
                SELECT url, date, news
                FROM news
                WHERE (date, url) > ($1, $2)
                  AND NOT EXISTS (
                    SELECT 1 FROM embs
                    WHERE embs.url = news.url AND embs.date = news.date
                  )
                ORDER BY date, url
                LIMIT $3
                """,
                last_date, last_url, batch_size
            )

            if not batch:
                return None

            news_texts = [news['news'] for news in batch]
            embeddings = await asyncio.to_thread(make_embs, news_texts)

            # Вставляем эмбеддинги
            await conn.executemany(
                """
                INSERT INTO embs (url, date, embedding)
                VALUES ($1, $2, $3)
                ON CONFLICT (url, date) DO NOTHING
                """,
                [(news['url'], news['date'], embedding) for news, embedding in zip(batch, embeddings)]
            )

            last_processed = batch[-1]
            await update_last_processed(conn, last_processed['url'], last_processed['date'])

            return last_processed['url'], last_processed['date']

    conn = await asyncpg.connect(**db_config)
    try:
        # Создаем таблицу для хранения последней обработанной записи, если её нет
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS last_processed_news (
                id INTEGER PRIMARY KEY DEFAULT 1,
                url TEXT,
                date TIMESTAMP WITHOUT TIME ZONE,
                CONSTRAINT single_row CHECK (id = 1)
            )
            """
        )

        last_processed = await get_last_processed(conn)
        last_url = last_processed['url'] if last_processed else ''
        last_date = last_processed['date'] if last_processed else datetime.min

        while True:
            result = await process_batch(conn, last_url, last_date)
            if not result:
                break
            last_url, last_date = result
            print(f"Processed batch up to {last_date}")

    finally:
        await conn.close()


# Использование
db_config = {
    'host': 'DB_HOST',
    'database': 'DB_NAME',
    'user': 'DB_USER',
    'password': 'DB_PASS'
}

asyncio.run(process_news_embeddings(db_config))
