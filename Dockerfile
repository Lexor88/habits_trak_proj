FROM python:3.12.3

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

# Копируем весь проект
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]