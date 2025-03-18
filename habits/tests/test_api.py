from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser  # Импортируем кастомную модель пользователя
from habits.models import Habit  # Импортируем модель привычки


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
