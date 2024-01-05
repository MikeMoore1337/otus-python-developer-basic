# Create your views here.
from django.shortcuts import render

from .models import Car


def cars(request):
    car = Car.objects.all()
    return render(request, 'cars/catalog.html', {'cars': car})
