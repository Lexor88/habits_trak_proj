from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path(
        "register/", RegisterView.as_view(), name="register"
    ),  # Эндпоинт для регистрации
    path("login/", LoginView.as_view(), name="login"),  # Эндпоинт для логина
]