from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Habit
from .serializers import HabitSerializer
from .pagination import HabitPagination


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]  # Все запросы требуют авторизации
    pagination_class = HabitPagination

    def get_queryset(self):
        """Возвращает привычки пользователя и публичные привычки."""
        user = self.request.user
        if user.is_authenticated:
            return Habit.objects.filter(user=user) | Habit.objects.filter(is_public=True)
        raise PermissionDenied("You do not have access to this habit")

    def perform_create(self, serializer):
        """При создании привычки связываем с текущим пользователем."""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Пользователь может редактировать только свои привычки."""
        habit = self.get_object()
        if habit.user != self.request.user:
            raise PermissionDenied("You can only edit your own habits.")
        serializer.save()

    def perform_destroy(self, instance):
        """Пользователь может удалять только свои привычки."""
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own habits.")
        instance.delete()