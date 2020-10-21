from rest_framework import serializers
from aviata.flights.models import Flight, Airport, Direction


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class DirectionSerializer(serializers.ModelSerializer):
    fly_to = AirportSerializer()
    fly_from = AirportSerializer()

    class Meta:
        model = Direction
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    direction = DirectionSerializer()

    class Meta:
        model = Flight
        fields = "__all__"
