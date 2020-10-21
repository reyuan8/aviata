from django.apps import AppConfig


class FlightConfig(AppConfig):

    name = 'aviata.flights'
    verbose_name = 'Flight'

    def ready(self):
        try:
            import aviata.flights.signals  # noqa F401
        except ImportError:
            pass
