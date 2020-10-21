from django.core.management import BaseCommand

from aviata.flights.consts import directions
from aviata.flights.models import Direction, Airport


class Command(BaseCommand):
    def handle(self, *args, **options):

        for direction in directions:
            Direction.objects.get_or_create(
                fly_from=Airport.objects.get(code=direction[0]),
                fly_to=Airport.objects.get(code=direction[1])
            )
