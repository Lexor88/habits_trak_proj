from celery import Celery
from celery.schedules import crontab  # Для периодического задания

# Устанавливаем настройки Django для использования Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracker.settings")

# Создаем экземпляр приложения Celery
app = Celery("tracker")

# Загружаем настройки из файла settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Устанавливаем расписание для периодической задачи
app.conf.beat_schedule = {
    "send-reminders-every-day": {
        "task": "habits.tasks.send_habit_reminders",  # Указываем путь к задаче
        "schedule": crontab(
            minute=0, hour=9
        ),  # Отправка напоминаний каждый день в 9 утра
    },
}

# Автоматически обнаруживаем задачи в приложениях Django
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
