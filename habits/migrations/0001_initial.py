# Generated by Django 4.2.20 on 2025-03-18 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Habit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("place", models.CharField(max_length=255)),
                ("time", models.TimeField()),
                ("action", models.TextField()),
                ("is_pleasant", models.BooleanField(default=False)),
                ("periodicity", models.PositiveIntegerField(default=1)),
                ("reward", models.CharField(blank=True, max_length=255, null=True)),
                ("execution_time", models.PositiveIntegerField(default=120)),
                ("is_public", models.BooleanField(default=False)),
                (
                    "related_habit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="habits.habit",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
