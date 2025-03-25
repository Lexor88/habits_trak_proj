from __future__ import absolute_import, unicode_literals

# Это необходимо для того, чтобы приложение Celery загружалось при старте проекта
from config.celery import app as celery_app

__all__ = ("celery_app",)
