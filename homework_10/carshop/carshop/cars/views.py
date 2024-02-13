# Create your views here.
from django.views.generic import DetailView, ListView

from .models import Car


class CarListView(ListView):
    model = Car
    template_name = 'cars/catalog.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
