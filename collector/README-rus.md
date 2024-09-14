# News Collector

![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Docker](https://img.shields.io/badge/docker-compatible-brightgreen.svg)

News Collector - это асинхронный скрипт на Python для сбора, обработки и хранения новостей из различных источников.

## Особенности

- 🔄 Асинхронный сбор новостей
- 🧹 Очистка и обработка текста новостей
- 🏷️ Автоматическая категоризация новостей
- 📊 Генерация эмбеддингов для новостей
- 📝 Создание кратких резюме новостей
- 🗓️ Работа по расписанию (каждый час)
- 🐳 Поддержка Docker

## Требования

- Python 3.9+
- PostgreSQL
- Docker (опционально)

## Установка

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/your-username/news-collector.git
   cd news-collector
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```
   python -m venv venv
   source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные окружения:
   ```
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASS=your_database_password
   DB_HOST=your_database_host
   DB_PORT=your_database_port
   ```

## Использование

### Запуск скрипта

Для запуска скрипта выполните:

```
python main.py
```

Скрипт будет запускаться каждый час для сбора и обработки новых новостей.

### Использование Docker

1. Соберите Docker-образ:
   ```
   docker-compose build
   ```

2. Запустите контейнеры:
   ```
   docker-compose up -d
   ```

## Структура проекта

```
news-collector/
│
├── api/
│   └── client.py
├── db/
│   └── database.py
├── models/
│   └── news_item.py
├── news/
│   ├── parser.py
│   └── processor.py
├── .env
├── docker-compose.yaml
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

## Описание модулей

- `api/client.py`: Клиент для взаимодействия с API новостных сервисов
- `db/database.py`: Управление подключением к базе данных и операциями с ней
- `models/news_item.py`: Модель данных для новостных статей
- `news/parser.py`: Парсер для извлечения новостей из HTML
- `news/processor.py`: Обработчик новостей (категоризация, генерация эмбеддингов и т.д.)
- `main.py`: Основной скрипт, управляющий процессом сбора новостей

## Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста, следуйте этим шагам:

1. Форкните репозиторий
2. Создайте ветку для вашей функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте ваши изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте изменения в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## Лицензия

Распространяется по лицензии MIT. Смотрите `LICENSE` для получения дополнительной информации.

