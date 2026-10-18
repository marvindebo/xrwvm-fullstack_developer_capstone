from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = [
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("Wagon", "Wagon"),
        ("Coupe", "Coupe"),
        ("Hatchback", "Hatchback"),
        ("Truck", "Truck"),
        ("Convertible", "Convertible"),
        ("Other", "Other"),
    ]

    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name="models"
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=CAR_TYPES)
    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2023)
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
