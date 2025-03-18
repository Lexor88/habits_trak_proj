from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("action", "user", "time", "is_public")
    search_fields = ("action", "user__username")
    list_filter = ("is_public", "is_pleasant")
