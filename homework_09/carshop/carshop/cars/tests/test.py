from django.test import TestCase

from ..models import Car


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.car_data = {
            'brand': 'Toyota',
            'model': 'Camry',
            'year': 2022,
            'price': 30000.00,
        }
        cls.car = Car.objects.create(**cls.car_data)

    @classmethod
    def tearDownClass(cls):
        cls.car.delete()
        super().tearDownClass()

    def test_car_creation(self):
        car = Car.objects.get(brand='Toyota', model='Camry', year=2022, price=30000.00)
        self.assertEqual(str(car), 'Toyota Camry (2022) - 30000.00')

    def test_car_str_method(self):
        self.assertEqual(str(self.car), 'Toyota Camry (2022) - 30000.00')
