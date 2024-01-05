from django.urls import path

from .views import cars

urlpatterns = [
    path("catalog.html", cars, name="catalog"),
    # Другие URL-шаблоны, если они есть
]
