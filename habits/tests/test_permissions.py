from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from habits.models import Habit
from users.models import CustomUser


class HabitPermissionsTest(APITestCase):

    def setUp(self):
        self.owner = CustomUser.objects.create_user(
            username="owner", email="owner@test.com", password="password"
        )
        self.other_user = CustomUser.objects.create_user(
            username="other", email="other@test.com", password="password"
        )
        self.habit = Habit.objects.create(
            user=self.owner,
            place="home",
            action="run",
            time="08:00",
            reward="chocolate",
            execution_time=120,
            is_pleasant=False,
            periodicity=1,
            is_public=False,
        )

    def test_access_control(self):
        """Проверим, что только владелец может редактировать и удалять свои привычки"""
        self.client.force_authenticate(user=self.other_user)
        url = reverse("habit-detail", args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Доступ только для владельца
