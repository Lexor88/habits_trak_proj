# config/views.py
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1>Welcome to the Habit config API</h1>")
