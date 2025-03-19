from celery import shared_task
from datetime import datetime
import requests
import os


@shared_task
def send_habit_reminders():
    # Загружаем переменную окружения
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables!")

    from habits.models import Habit  # Переносим импорт модели сюда

    now = datetime.now().time()
    habits = Habit.objects.filter(time__lte=now)

    print(f"⏰ Сейчас: {now}")  # Добавляем отладку
    print(f"🔍 Найдено привычек: {habits.count()}")  # Покажет, сколько привычек нашлось

    for habit in habits:
        print(f"📤 Отправляем сообщение для {habit.user}")  # Логируем пользователя
        # Добавляем вывод отладочного сообщения
        print("Sending reminder task for user:", habit.user)  # Это строка для отладки
        if habit.user.telegram_chat_id:
            message = f"🔔 Напоминание: {habit.action} в {habit.place}"
            response = requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                data={"chat_id": habit.user.telegram_chat_id, "text": message},
            )
            print(f"✅ Ответ Telegram API: {response.status_code}, {response.text}")