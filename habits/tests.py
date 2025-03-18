from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser  # Импортируем кастомную модель пользователя
from habits.models import Habit  # Импортируем модель привычки
from django.core.exceptions import ValidationError
from django.test import TestCase


class HabitTests(APITestCase):

    def setUp(self):
        # Создаем тестового пользователя с обязательным полем username
        self.user = CustomUser.objects.create_user(
            username="testuser",  # Обязательное поле
            email="test@user.com",
            password="testpassword",
        )

        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        url = reverse("habit-list")  # URL для создания привычки

        # Данные для создания привычки (обновляем, добавляя обязательные поля)
        data = {
            "name": "Тестовая привычка",
            "place": "В тесте",
            "action": "Протестировать",
            "first_time_to_do": "2024-09-02T19:10:04.709123+03:00",
            "reward": "Тест пройден",
            "related_habit": None,
            "is_pleasant": False,
            "periodicity": 1,
            "execution_time": 120,
            "is_public": False,
            "is_active": False,
            "user": self.user.id,  # передаем пользователя
            "time": "08:00:00",  # передаем время (обратите внимание на формат времени)
        }

        # Отправляем POST запрос на создание привычки
        response = self.client.post(url, data, format="json")

        # Выводим содержимое ответа для диагностики
        print(response.data)

        # Проверяем, что ответ имеет статус 201 (создание успешно)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        class HabitModelTest(TestCase):
            def setUp(self):
                """Создаем пользователя для теста"""
                self.user = CustomUser.objects.create(
                    email="testuser@example.com",
                    username="testuser",
                    password="testpassword",
                )

            def test_create_habit(self):
                """Тестируем создание привычки"""
                habit = Habit.objects.create(
                    user=self.user,
                    place="home",
                    time="08:00:00",
                    action="run",
                    reward="chocolate",
                    execution_time=120,
                    is_public=False,
                )
                self.assertEqual(habit.place, "home")
                self.assertEqual(habit.time.strftime("%H:%M:%S"), "08:00:00")
                self.assertEqual(habit.action, "run")
                self.assertEqual(habit.reward, "chocolate")

            def test_habit_invalid_duration(self):
                """Тестируем валидацию: время на выполнение не может быть больше 120 секунд"""
                habit = Habit(
                    user=self.user,
                    place="home",
                    time="08:00:00",
                    action="run",
                    reward="chocolate",
                    execution_time=130,  # больше 120
                    is_public=False,
                )
                with self.assertRaises(ValidationError):
                    habit.full_clean()  # Проверка на валидацию

            def test_habit_reward_and_related_habit(self):
                """Тестируем, что нельзя указать и вознаграждение, и связанную привычку одновременно"""
                habit = Habit(
                    user=self.user,
                    place="home",
                    time="08:00:00",
                    action="run",
                    reward="chocolate",
                    related_habit=None,
                    # Здесь нельзя заполнять оба поля, так как только одно из них может быть заполнено
                    execution_time=120,
                    is_public=False,
                )
                with self.assertRaises(ValidationError):
                    habit.full_clean()

            def test_periodicity_valid_range(self):
                """Тестируем валидацию: периодичность должна быть от 1 до 7"""
                habit = Habit(
                    user=self.user,
                    place="home",
                    time="08:00:00",
                    action="run",
                    reward="chocolate",
                    periodicity=0,  # Неверная периодичность
                    execution_time=120,
                    is_public=False,
                )
                with self.assertRaises(ValidationError):
                    habit.full_clean()

            def test_periodicity_valid_range_high(self):
                """Тестируем валидацию: периодичность должна быть от 1 до 7"""
                habit = Habit(
                    user=self.user,
                    place="home",
                    time="08:00:00",
                    action="run",
                    reward="chocolate",
                    periodicity=8,  # Неверная периодичность
                    execution_time=120,
                    is_public=False,
                )
                with self.assertRaises(ValidationError):
                    habit.full_clean()


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
