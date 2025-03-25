from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet

# Регистрируем маршруты для HabitViewSet
router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")

urlpatterns = [
    path("", include(router.urls)),  # Включаем маршруты для HabitViewSet
]