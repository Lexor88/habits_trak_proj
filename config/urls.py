from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Для редиректа на главную страницу
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Схема для документации API (Swagger, ReDoc)
schema_view = get_schema_view(
    openapi.Info(
        title="Habits API",
        default_version="v1",
        description="Документация для API приложения привычек",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@habits.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # Разрешаем доступ всем
)

urlpatterns = [
    path("admin/", admin.site.urls),  # Страница администрирования
    path("api/", include("habits.urls")),  # API для привычек
    path("api/users/", include("users.urls")),  # API для пользователей
    path("", RedirectView.as_view(url="/api/")),  # Редирект на API
    # Swagger и ReDoc документация
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
