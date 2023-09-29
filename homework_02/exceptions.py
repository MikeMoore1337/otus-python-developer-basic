"""
Объявите следующие исключения:
- LowFuelError
- NotEnoughFuel
- CargoOverload
"""


class LowFuelError(Exception):
    def __init__(self, message="Not enough fuel to start"):
        super().__init__(message)


class NotEnoughFuel(Exception):
    def __init__(self, message="Not enough fuel to cover the distance"):
        super().__init__(message)


class CargoOverload(Exception):
    def __init__(self, message="Cargo capacity exceeded"):
        super().__init__(message)
