from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    time = models.TimeField()  # Время для выполнения привычки
    action = models.TextField()
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    periodicity = models.PositiveIntegerField(
        default=1
    )  # Периодичность (1 - ежедневно, 2 - раз в 2 дня и т.д.)
    reward = models.CharField(max_length=255, blank=True, null=True)
    execution_time = models.PositiveIntegerField(default=120)  # Время выполнения (не более 120 секунд)
    is_public = models.BooleanField(default=False)

    def clean(self):
        """Валидатор для проверки полей модели"""

        # Если привычка приятная, то нельзя одновременно указать вознаграждение или связанную привычку
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Pleasant habits cannot have a reward or related habit.")

        # Если привычка полезная (не приятная), то должно быть либо вознаграждение, либо связанная привычка
        if not self.is_pleasant:
            if not (self.reward or self.related_habit):
                raise ValidationError("Useful habits must have either a reward or a related habit.")

            # Полезная привычка не может иметь одновременно и вознаграждение, и связанную привычку
            if self.reward and self.related_habit:
                raise ValidationError("Useful habits cannot have both a reward and a related habit.")

            # Связанная привычка должна быть приятной
            if self.related_habit and not self.related_habit.is_pleasant:
                raise ValidationError("Related habits must be pleasant.")

        # Время выполнения привычки не должно превышать 120 секунд
        if self.execution_time > 120:
            raise ValidationError("Execution time should not exceed 120 seconds.")

        # Периодичность привычки должна быть в пределах от 1 до 7 дней
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError("Periodicity must be between 1 and 7 days.")

        # После выполнения всех проверок вызываем super() для стандартной очистки
        super().clean()

    def __str__(self):
        return f"{self.action} ({self.user.username})"