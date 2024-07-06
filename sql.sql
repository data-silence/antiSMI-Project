-- РАЗДЕЛ I: НОРМАЛИЗАЦИЯ ТАБЛИЦ

-- Шаг 1: Создание временной таблицы с уникальными строками (исключение дублей)
CREATE TEMP TABLE temp_table AS
SELECT DISTINCT ON (url) *
FROM news;

-- Шаг 2: Удаление всех строк из оригинальной таблицы
TRUNCATE TABLE news;

-- Шаг 3: Вставка уникальных строк обратно в оригинальную таблицу
INSERT INTO news
SELECT * FROM temp_table;

-- Удаление временной таблицы
DROP TABLE temp_table;



-- Преобразование типа ссылок из списка в массив
ALTER TABLE news
ADD COLUMN links_array TEXT[];

UPDATE news
SET links_array = string_to_array(links, ', ');


ALTER TABLE news
DROP COLUMN links;


ALTER TABLE news
RENAME COLUMN links_array TO links;


-- Переименование прежней таблицы и создание новой с необходимой структурой данных

ALTER TABLE news RENAME TO old_news_table;


CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    resume TEXT,
    news TEXT,
    date TIMESTAMP WITHOUT TIME ZONE,
    agency_id INTEGER NOT NULL REFERENCES agencies(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    links TEXT[]
);



-- ПРИВЕДЕНИЕ ОСТАЛЬНЫХ ТАБЛИЦ К НЕОБХОДИМОМУ ВИДУ


-- Шаг 1: Проверка уникальности значений в столбце id
SELECT id, COUNT(*)
FROM agencies
GROUP BY id
HAVING COUNT(*) > 1;

-- Шаг 2: Установка столбца id в качестве первичного ключа
ALTER TABLE agencies ADD PRIMARY KEY (id);

-- Шаг 3: Настройка последовательности для автоматической генерации уникальных значений
CREATE SEQUENCE agencies_id_seq START WITH (SELECT MAX(id) + 1 FROM categories);
ALTER TABLE agencies ALTER COLUMN id SET DEFAULT nextval('agencies_id_seq');

-- Выполнение запроса для получения имени столбца первичного ключа

-- 1. Добавить новый столбец id с типом SERIAL
ALTER TABLE categories ADD COLUMN id SERIAL;

-- 2. Обновить таблицу, назначив новый столбец id в качестве первичного ключа
ALTER TABLE categories ADD PRIMARY KEY (id);

-- 3. Добавить уникальное ограничение на столбец category
ALTER TABLE categories ADD CONSTRAINT unique_category UNIQUE (category);
SET date = date AT TIME ZONE 'Europe/Moscow' AT TIME ZONE 'UTC';



-- ПЕРЕНОС ДАННЫХ В НОВУЮ ТАБЛИЦУ ИЗ СТАРОЙ, УДАЛЕНИЕ СТАРОЙ ТАБЛИЦЫ

INSERT INTO news (url, title, resume, news, date, agency_id, category_id, links)
SELECT
    url,
    title,
    resume,
    news,
    old_news_table.date AT TIME ZONE 'Europe/Moscow' AT TIME ZONE 'UTC', -- Преобразование времени в UTC
    (SELECT id FROM agencies WHERE telegram = old_news_table.agency),
    (SELECT id FROM categories WHERE category = old_news_table.category),
    links
FROM old_news_table;

DROP TABLE old_news_table;


-- РАЗДЕЛ II: ПРЕДСТАВЛЕНИЯ, ПРАВИЛА, ТРИГГЕРЫ ДЛЯ СОВМЕСТИМОСТИ ПРЕЖНЕЙ РАБОТЫ С ТЕКУЩЕЙ СТРУКТУРОЙ

-- Создаем представление news_view, которое возвращает время в UTC
CREATE VIEW news_view AS
SELECT
    n.url,
    n.title,
    n.resume,
    n.news,
    n.date AS date, -- Возвращаем время в UTC, так как оно уже хранится в UTC в таблице news
    a.name AS agency,
    c.name AS category,
    array_to_string(n.links, ', ') AS links -- Преобразуем массив обратно в строку
FROM
    news n
JOIN
    agencies a ON n.agency_id = a.id
JOIN
    categories c ON n.category_id = c.id;


-- Правило для вставки в представление news_view
CREATE OR REPLACE RULE news_view_insert AS
ON INSERT TO news_view
DO INSTEAD
INSERT INTO news (url, title, resume, news, date, agency_id, category_id, links)
VALUES (
    NEW.url,
    NEW.title,
    NEW.resume,
    NEW.news,
    NEW.date AT TIME ZONE 'Europe/Moscow' AT TIME ZONE 'UTC', -- Преобразование даты в UTC
    (SELECT id FROM agencies WHERE telegram = NEW.agency),
    (SELECT id FROM categories WHERE category = NEW.category),
  	NEW.links
	-- COALESCE(string_to_array(NEW.links, ', '), NEW.links::text[]) -- Преобразование строкового списка в массив
);

-- Правило для обновления
CREATE OR REPLACE RULE news_view_update AS
ON UPDATE TO news_view
DO INSTEAD
UPDATE news
SET
    title = NEW.title,
    resume = NEW.resume,
    news = NEW.news,
    date = NEW.date AT TIME ZONE 'Europe/Moscow' AT TIME ZONE 'UTC', -- Преобразование даты в UTC
    agency_id = (SELECT id FROM agencies WHERE telegram = NEW.agency),
    category_id = (SELECT id FROM categories WHERE category = NEW.category),
    links = NEW.links -- Преобразование строкового списка в массив
WHERE url = NEW.url;

-- Правило для удаления
CREATE OR REPLACE RULE news_view_delete AS
ON DELETE TO news_view
DO INSTEAD
DELETE FROM news
WHERE url = OLD.url;


-- ПРИМЕРЫ ДЛЯ ТЕСТИРОВАНИЯ ПРАВИЛЬНОСТИ РАБОТЫ ПРЕДСТАВЛЕНИЯ

-- Вставка тестовых данных
INSERT INTO news_view (url, title, resume, news, date, agency, category, links)
VALUES (
    'https://example.com/news/1', -- URL
    'Test Title', -- Заголовок
    'Test Resume', -- Краткое содержание
    'Test News Content', -- Основное содержание новости
    '2024-07-06 12:00:00', -- Дата в московском времени
    'Lenta', -- Агентство (telegram идентификатор)
    'society', -- Категория
    '{https://example.com/source1, https://example.com/source2}' -- Ссылки на первоисточники через запятую
);


-- Обновление тестовых данных
UPDATE news_view
SET
    title = 'Updated Test Title',
    resume = 'Updated Test Resume',
    news = 'Updated Test News Content',
    date = '2024-07-07 12:00:00', -- Новая дата в московском времени
    agency = 'Lenta', -- Новое агентство
    category = 'sports', -- Новая категория
    links = '{https://example.com/source3, https://example.com/source4}' -- Новые ссылки на первоисточники
WHERE url = 'https://example.com/news/1';

-- Удаление тестовых данных
DELETE FROM news_view
WHERE url = 'https://example.com/news/1';

-- РАЗДЕЛ II: ПАРТИЦИРОВАНИЕ


-- Замена первичного ключа на составной первичный ключ
ALTER TABLE news DROP CONSTRAINT news_pkey;
ALTER TABLE news ADD PRIMARY KEY (url, date);

-- Создаём партицированную пустую таблицу с необходимой структурой
CREATE TABLE news_partitioned (
    url TEXT,
    title TEXT,
    resume TEXT,
    news TEXT NOT NULL,
    date TIMESTAMP WITHOUT TIME ZONE,
    agency_id INTEGER NOT NULL REFERENCES agencies(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    links TEXT[],
	PRIMARY KEY (url, date)
)  PARTITION BY RANGE (date);

-- Создаем партиции для каждого года, начиная с 1999 года и заканчивая 2030 годом

-- 1. 1999 год
CREATE TABLE news_y1999 PARTITION OF news_partitioned
    FOR VALUES FROM ('1999-01-01') TO ('2000-01-01');

-- 2. 2000 год
CREATE TABLE news_y2000 PARTITION OF news_partitioned
    FOR VALUES FROM ('2000-01-01') TO ('2001-01-01');
--

-- 5. 2029 год
CREATE TABLE news_y2029 PARTITION OF news_partitioned
    FOR VALUES FROM ('2029-01-01') TO ('2030-01-01');


-- Переносим данные:
INSERT INTO news_partitioned SELECT * FROM news;

-- Заменяем старую таблицу:
DROP TABLE news;
ALTER TABLE news_partitioned RENAME TO news;