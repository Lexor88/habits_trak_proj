from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("telegram_chat_id",)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
