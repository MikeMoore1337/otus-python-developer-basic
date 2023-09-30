"""
Объявите следующие исключения:
- LowFuelError
- NotEnoughFuel
- CargoOverload
"""


class BaseVehicleException(Exception):
    pass


class LowFuelError(BaseVehicleException):
    def __init__(self, message="Not enough fuel to start"):
        super().__init__(message)


class NotEnoughFuel(BaseVehicleException):
    def __init__(self, message="Not enough fuel to cover the distance"):
        super().__init__(message)


class CargoOverload(BaseVehicleException):
    def __init__(self, message="Cargo capacity exceeded"):
        super().__init__(message)
