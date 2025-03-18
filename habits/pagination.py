from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    page_size = 5  # Количество элементов на одну страницу
    page_size_query_param = "page_size"  # Параметр для указания размера страницы
    max_page_size = 100  # Максимальный размер страницы
