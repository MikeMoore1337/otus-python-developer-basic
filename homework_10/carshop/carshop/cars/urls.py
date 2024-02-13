from django.urls import path

from .views import CarListView, CarDetailView

urlpatterns = [
    path(
        "catalog.html",
        CarListView.as_view(),
        name="catalog"
    ),
    path(
        'car_detail/<int:pk>/',
        CarDetailView.as_view(),
        name='car_detail'
    ),
]
