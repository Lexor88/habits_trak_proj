from django_celery_beat.models import PeriodicTask, IntervalSchedule
from datetime import timedelta


def create_periodic_task():
    # Создаём интервал для задачи
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,  # Например, каждые 1 минуту
        period=IntervalSchedule.MINUTES,
    )

    # Создаем периодическую задачу
    PeriodicTask.objects.create(
        interval=schedule,  # Устанавливаем интервал
        name="send_habit_reminders",  # Имя задачи
        task="habits.tasks.send_habit_reminders",  # Имя задачи
    )


# Вызываем функцию создания задачи
create_periodic_task()
