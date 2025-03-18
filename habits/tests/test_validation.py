from django.test import TestCase
from django.core.exceptions import ValidationError
from habits.models import Habit
from users.models import CustomUser


class HabitValidationTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email="testuser@test.com", username="testuser", password="testpassword"
        )

    def test_invalid_duration(self):
        """Тестируем, что время на выполнение не может быть больше 120 секунд"""
        habit = Habit(
            user=self.user,
            place="home",
            time="08:00:00",
            action="run",
            reward="chocolate",
            execution_time=130,
        )
        with self.assertRaises(ValidationError):
            habit.clean()  # Должна возникнуть ошибка валидации

    def test_reward_and_related_habit(self):
        """Проверим, что нельзя указать и вознаграждение, и связанную привычку одновременно"""
        habit = Habit(
            user=self.user,
            place="home",
            time="08:00:00",
            action="study",
            reward="coffee",
            related_habit=self.habit,
        )
        with self.assertRaises(ValidationError):
            habit.clean()  # Ошибка, потому что оба поля заполнены

    def test_periodicity_valid_range(self):
        """Тестируем валидацию: периодичность должна быть от 1 до 7"""
        habit = Habit(
            user=self.user,
            place="home",
            time="08:00:00",
            action="run",
            reward="chocolate",
            periodicity=0,
            execution_time=120,
            is_public=False,
        )
        with self.assertRaises(ValidationError):
            habit.clean()  # Проверка на валидацию

    def test_periodicity_valid_range_high(self):
        """Тестируем валидацию: периодичность должна быть от 1 до 7"""
        habit = Habit(
            user=self.user,
            place="home",
            time="08:00:00",
            action="run",
            reward="chocolate",
            periodicity=8,
            execution_time=120,
            is_public=False,
        )
        with self.assertRaises(ValidationError):
            habit.clean()  # Проверка на валидацию
