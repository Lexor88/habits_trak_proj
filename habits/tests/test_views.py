from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from habits.models import Habit
from users.models import CustomUser


class HabitViewSetTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testuser@test.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)
        self.habit_data = {
            "action": "run",
            "place": "park",
            "time": "08:00",
            "reward": "chocolate",
            "execution_time": 120,
            "is_public": False,
        }

    def test_create_habit(self):
        url = reverse("habit-list")
        response = self.client.post(url, self.habit_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
