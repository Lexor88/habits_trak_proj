FROM python:3.12.3

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

# Копируем весь проект
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Создаем нового пользователя и группу
RUN groupadd -r celery && useradd -r -g celery celery

# Меняем владельца файлов на нового пользователя
RUN chown -R celery:celery /app

# Запускаем Celery от имени нового пользователя
USER celery