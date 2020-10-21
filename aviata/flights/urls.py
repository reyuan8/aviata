from django.urls import path

from aviata.flights.views import FlightView, AirportView, DirectionView, CheckFlight

app_name = 'flights'


urlpatterns = (
    path('all/', FlightView.as_view()),
    path('airports/', AirportView.as_view()),
    path('directions/', DirectionView.as_view()),
    path('check/', CheckFlight.as_view()),
)
