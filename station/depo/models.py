from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Crew(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Journey(models.Model):
    route = models.ForeignKey(
        "Route",
        on_delete=models.CASCADE,
        related_name="journey",
    )
    train = models.ForeignKey(
        "Train",
        on_delete=models.CASCADE,
        related_name="journey",
    )

    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(
        Crew,
        related_name="journey",
    )

    def __str__(self):
        return f"{self.route}. Train: {self.train}"


class Train(models.Model):
    name = models.CharField(max_length=100)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(
        "TrainType",
        on_delete=models.CASCADE,
        related_name="train",
    )

    def __str__(self):
        return self.name


class TrainType(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.name


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()

    journey = models.ForeignKey(
        "Journey",
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="tickets",
    )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="orders",
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Route(models.Model):
    source = models.ForeignKey(
        "Station",
        on_delete=models.CASCADE,
        related_name="route_from",
    )
    destination = models.ForeignKey(
        "Station",
        on_delete=models.CASCADE,
        related_name="route_to",
    )
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source} - {self.destination}"


class Station(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
