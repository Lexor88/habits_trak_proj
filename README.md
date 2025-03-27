🧠 Habit Config

Описание

Habit Config — это веб-приложение для отслеживания полезных привычек. Пользователи могут создавать привычки, получать напоминания и отслеживать их выполнение. Проект реализован на Django и Django REST Framework, с Celery и Redis для отложенных задач, а также с интеграцией с Telegram для уведомлений.

🚀 Функциональность
	•	✅ Создание и редактирование привычек
	•	📋 Просмотр списка привычек с пагинацией
	•	🤖 Уведомления через Telegram-бота
	•	⏱ Проверка ограничения по времени выполнения привычки (не более 120 секунд)
	•	🔒 Приватность (пользователь видит только свои привычки)
	•	🔁 Поддержка периодичности привычек

🛠 Технологии
	•	Python 3.9+
	•	Django 4.2
	•	Django REST Framework
	•	PostgreSQL (или SQLite для локальной разработки)
	•	Redis (брокер для Celery)
	•	Celery (асинхронные задачи)
	•	Telegram Bot API
	•	Docker & Docker Compose
	•	Flake8 / Black / Coverage

⸻
📦 Установка и запуск локально
	1.	Клонируйте репозиторий:
git clone https://github.com/yourusername/habit-config.git
cd habit-config

## Развертывание

Для развертывания проекта на сервере используйте Docker. Приложение доступно по следующему адресу:

[http://158.160.90.60:8000](http://158.160.90.60:8000)
.	Создайте файл .env по образцу:
# .env

POSTGRES_DB=my_database
POSTGRES_USER=my_user
POSTGRES_PASSWORD=my_password

REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

SECRET_KEY=my_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1, .localhost

TELEGRAM_BOT_TOKEN=your_telegram_token

3.	Запуск через Docker:
Убедитесь, что Docker и Docker Compose установлены, затем:
docker-compose up --build

	4.	Приложение будет доступно по адресу:
http://localhost:8000

⚙️ Проверка работоспособности
	•	Django: http://localhost:8000
	•	Redis: порт 6379 (можно проверить через redis-cli)
	•	PostgreSQL: доступ через:
docker-compose exec db psql -U my_user -d my_database
	•	Celery: статус можно проверить:
docker-compose exec celery celery -A config status

🚦 Миграции

Миграции выполняются автоматически при запуске благодаря команде:
command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"


🔁 CI/CD через GitHub Actions

Проект настроен на автоматическое тестирование и деплой при пуше в репозиторий.

✅ Этапы workflow:

1. Тестирование
	•	Используется PostgreSQL в контейнере
	•	Установка зависимостей
	•	Запуск тестов:python manage.py test



2. Автоматический деплой на сервер
	•	Подключение по SSH
	•	Обновление проекта на сервере
	•	Перезапуск Docker-контейнеров

📂 Структура workflow: .github/workflows/ci-cd.yml

name: Django CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: postgres
        ports: ['5432:5432']
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5

    steps:
      - name: Check out code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: python manage.py test
        env:
          POSTGRES_DB: ${{ secrets.POSTGRES_DB }}
          POSTGRES_USER: ${{ secrets.POSTGRES_USER }}
          POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
          POSTGRES_HOST: ${{ secrets.POSTGRES_HOST }}
          POSTGRES_PORT: ${{ secrets.POSTGRES_PORT }}
          SECRET_KEY: ${{ secrets.SECRET_KEY }}

  deploy:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - name: Set up SSH
        uses: webfactory/ssh-agent@v0.9.0
        with:
          ssh-private-key: ${{ secrets.SSH_KEY }}

      - name: Deploy to server
        run: |
          sshpass -p root ssh -v -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} "cd habits_trak_proj && git pull" << 'EOF'
          docker compose down
          docker container prune -f
          docker image prune -f
          docker network prune -f
          docker volume prune -f
          docker rmi mypedia
          docker compose up -d --build
          EOF