from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)


class Direction(models.Model):
    fly_from = models.ForeignKey(
        to='flights.Airport',
        related_name='fly_from',
        on_delete=models.CASCADE
    )
    fly_to = models.ForeignKey(
        to='flights.Airport',
        related_name='fly_to',
        on_delete=models.CASCADE
    )


class Flight(models.Model):
    flight_id = models.CharField(max_length=200, unique=True)
    flight_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    fly_duration = models.CharField(blank=True, max_length=50)

    price = models.CharField(max_length=50)
    booking_token = models.TextField()
    direction = models.ForeignKey(
        to='flights.Direction',
        related_name='directions',
        on_delete=models.CASCADE
    )
