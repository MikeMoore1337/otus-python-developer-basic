from django.db import models


# Create your models here.
class Engine(models.Model):
    class Meta:
        verbose_name_plural = "Engine type"

    type = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.type


class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    engine = models.ForeignKey(
        Engine,
        on_delete=models.CASCADE,
        related_name="cars",
    )

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) - {self.price}"
