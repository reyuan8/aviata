from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from aviata.flights.models import Flight, Airport, Direction
from aviata.flights.serializers import FlightSerializer, AirportSerializer, DirectionSerializer

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from aviata.flights.utils import check_flight


class FlightView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = FlightSerializer

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*60*2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        print('Using db!!!')

        qs = Flight.objects.all()

        if self.request.query_params.get('direction'):
            qs = qs.filter(direction=self.request.query_params.get('direction'))

        return qs.order_by('price')


class AirportView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()


class DirectionView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = DirectionSerializer
    queryset = Direction.objects.all()


class CheckFlight(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        if self.request.query_params.get('flight'):
            flight = Flight.objects.get(pk=self.request.query_params.get('flight'))
            r = check_flight(flight.booking_token)
        else:
            r = {'Must be field [flight] in query_params'}
        return Response(r)
