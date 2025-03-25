Habit Tracker

Описание

Проект Habit Tracker — это веб-приложение для отслеживания полезных привычек. Пользователи могут создавать привычки,
получать напоминания и отслеживать их выполнение. Это приложение является учебным проектом, реализованным с
использованием Django и Django REST Framework для бэкенда, Celery для отложенных задач, и интеграцией с Telegram для
отправки уведомлений.

Функции
• Создание и редактирование привычек.
• Отображение списка привычек с пагинацией.
• Интеграция с Telegram для отправки уведомлений о привычках.
• Поддержка валидации данных (например, время выполнения привычки не может превышать 120 секунд).
• Приватность привычек (пользователь может видеть только свои привычки).
• Поддержка периодичности привычек.

Технологии
• Python 3.9+
• Django 4.2
• Django REST Framework
• Celery (для отложенных задач)
• Redis (для брокера сообщений Celery)
• PostgreSQL (или SQLite для разработки)
• Telegram API
• Flake8 для линтинга
• Coverage для покрытия тестами
• Black для автоформатирования кода

Установка

1. Клонируйте репозиторий:
   git clone https://github.com/yourusername/habit-tracker.git
   cd habit-tracker
2. Создайте файл .env

# PostgreSQL Database Credentials

POSTGRES_DB=my_database
POSTGRES_USER=my_user
POSTGRES_PASSWORD=my_password

# Redis URL

REDIS_URL=redis://localhost:6379/0

# Celery settings

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Django settings

SECRET_KEY=my_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1, .localhost

# Telegram Bot Token (если используете)

TELEGRAM_BOT_TOKEN=your_telegram_token

3. Использование Docker

Для упрощения процесса развертывания проекта, используйте Docker. Убедитесь, что у вас установлен Docker и Docker
Compose.

Шаги по запуску проекта через Docker:
Соберите и запустите контейнеры:
docker-compose up --build

2. После того как контейнеры будут готовы, приложение будет доступно по адресу:
   http://localhost:8000

4.Проверка работоспособности сервисов:
• Django: Перейдите по http://localhost:8000, чтобы убедиться, что сервер работает.
• Redis: Redis должен быть доступен на порту 6379. Вы можете использовать команду redis-cli для проверки соединения:
redis-cli -h localhost -p 6379
docker-compose exec db psql -U my_user -d my_database
docker-compose exec celery celery -A config status

4. Запуск миграций

В Docker контейнерах выполнение миграций осуществляется автоматически при запуске контейнера с командой в
docker-compose.yml:
command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"

5. Остановка всех сервисов
   docker-compose down
6. Повторный запуск с изменениями

Если вы внесли изменения и хотите пересобрать контейнеры, выполните:
docker-compose up --build