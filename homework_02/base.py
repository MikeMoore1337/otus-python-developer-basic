from abc import ABC
from exceptions import LowFuelError, NotEnoughFuel


class Vehicle(ABC):
    def __init__(self, weight=0, fuel=0, fuel_consumption=1):
        self.weight = weight
        self.started = False
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption

    def start(self):
        if not self.started:
            if self.fuel > 0:
                self.started = True
            else:
                raise LowFuelError

    def move(self, distance):
        if self.started:
            required_fuel = self.fuel_consumption * distance
            if self.fuel >= required_fuel:
                self.fuel -= required_fuel
            else:
                raise NotEnoughFuel
        else:
            raise ValueError("Vehicle must be started before moving")
