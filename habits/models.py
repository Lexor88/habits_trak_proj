from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    time = models.TimeField()  # Убедитесь, что это поле времени, а не строка
    action = models.TextField()
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    periodicity = models.PositiveIntegerField(
        default=1
    )  # 1 - ежедневно, 2 - раз в 2 дня и т.д.
    reward = models.CharField(max_length=255, blank=True, null=True)
    execution_time = models.PositiveIntegerField(default=120)  # Не более 120 секунд
    is_public = models.BooleanField(default=False)

    def clean(self):
        """Валидатор для проверки полей модели"""
        if self.reward and self.related_habit:
            raise ValidationError(
                "Either reward or related habit should be provided, not both."
            )
        if self.execution_time > 120:
            raise ValidationError("Execution time should not exceed 120 seconds.")
        if self.is_pleasant and self.reward:
            raise ValidationError("Pleasant habits should not have a reward.")
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Related habit must be pleasant.")
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError("Periodicity must be between 1 and 7 days.")

    def __str__(self):
        return f"{self.action} ({self.user.username})"
