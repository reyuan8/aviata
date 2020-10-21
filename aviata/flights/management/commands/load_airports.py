from django.core.management import BaseCommand

from aviata.flights.consts import airports
from aviata.flights.models import Airport


class Command(BaseCommand):
    def handle(self, *args, **options):

        for airport in airports:
            Airport.objects.get_or_create(name=airport[0], code=airport[1])
