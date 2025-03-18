from django.test import TestCase
from django.core.exceptions import ValidationError
from habits.models import Habit
from users.models import CustomUser


class HabitModelTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            email="testuser@test.com", username="testuser", password="testpassword"
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place="home",
            action="run",
            time="08:00",
            reward="chocolate",
            execution_time=120,
            is_pleasant=False,
            periodicity=1,
            is_public=False,
        )

    def test_habit_creation(self):
        """Тестируем создание привычки"""
        habit = Habit.objects.get(id=self.habit.id)
        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.place, "home")
        self.assertEqual(habit.action, "run")
        self.assertEqual(habit.reward, "chocolate")
        self.assertEqual(habit.execution_time, 120)
        self.assertEqual(habit.is_pleasant, False)
        self.assertEqual(habit.periodicity, 1)

    def test_invalid_execution_time(self):
        """Проверим, что время выполнения не может быть больше 120 секунд"""
        habit = Habit(
            user=self.user, place="gym", action="jump", time="09:00", execution_time=130
        )
        with self.assertRaises(ValidationError):
            habit.clean()  # Должна возникнуть ошибка валидации

    def test_reward_and_related_habit(self):
        """Проверим, что нельзя указать и вознаграждение, и связанную привычку одновременно"""
        habit = Habit(
            user=self.user,
            place="home",
            action="study",
            reward="coffee",
            related_habit=self.habit,
        )
        with self.assertRaises(ValidationError):
            habit.clean()  # Ошибка, потому что оба поля заполнены

    def test_valid_habit(self):
        """Проверим, что привычка проходит валидацию"""
        habit = Habit(
            user=self.user,
            place="office",
            action="write",
            time="10:00",
            reward="break",
            execution_time=100,
        )
        try:
            habit.clean()  # Не должна возникнуть ошибка
        except ValidationError:
            self.fail("Valid habit raised ValidationError unexpectedly!")
