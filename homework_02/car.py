"""
создайте класс `Car`, наследник `Vehicle`
"""
from abc import ABC
from base import Vehicle
from engine import Engine


class Car(Vehicle):
    def __init__(self, weight=1000, fuel=50, fuel_consumption=5):
        super().__init__(weight, fuel, fuel_consumption)
        self.engine = None

    def set_engine(self, engine: Engine):
        self.engine = engine
