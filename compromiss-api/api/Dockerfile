FROM python:3.12.2-slim

WORKDIR /app

# Устанавливаем зависимости и необходимые пакеты
RUN apt-get update && apt-get install -y --no-install-recommends \
        mc \
        curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip

# Копируем только requirements.txt сначала для использования кеша Docker
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . ./api/.

# Устанавливаем метку
LABEL authors="data-silence"

# Команда для запуска приложения
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "2", "--timeout-keep-alive", "3600"]
#CMD ["uvicorn", "-w", "2", "-k", "api.main:app", "0.0.0.0:8001", "--timeout", "3600"]