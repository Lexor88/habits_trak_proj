FROM python:3.12.3

WORKDIR /app

# Устанавливаем системные пакеты
RUN apt update && apt install -y gcc libpq-dev

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

EXPOSE 8000

# Меняем владельца файлов
RUN groupadd -r celery && useradd -r -g celery celery
RUN chown -R celery:celery /app && chmod -R 755 /app

# Запускаем Celery от имени нового пользователя
USER celery

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]