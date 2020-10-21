import requests
import datetime
from aviata.flights.consts import directions
from aviata.flights.models import Direction, Flight


SEARCH_API = 'https://api.skypicker.com/flights'
CHECK_API = 'https://booking-api.skypicker.com/api/v0.1/check_flights?'
PARTNER = 'picky'


def create_flight(result):

    flight_time_ts = result.get('dTime')
    arrival_time_ts = result.get('aTime')

    direction = Direction.objects.get(
        fly_from__code=result.get('cityCodeFrom'),
        fly_to__code=result.get('cityCodeTo')
    )

    data = {
        'flight_id': result.get('id'),
        'flight_time': datetime.datetime.fromtimestamp(flight_time_ts),
        'arrival_time': datetime.datetime.fromtimestamp(arrival_time_ts),
        'fly_duration': result.get('fly_duration'),
        'price': result.get('price'),
        'booking_token': result.get('booking_token'),
        'direction': direction
    }

    flight = Flight.objects.create(**data)
    print(flight.id)


def get_flights():

    for direction in directions:
        fly_from = direction[0]
        fly_to = direction[1]

        date_from = datetime.datetime.now()
        date_to = date_from + datetime.timedelta(days=30)
        data = {
            'flyFrom': fly_from,
            'to': fly_to,
            'dateFrom': date_from.strftime("%d/%m/%Y"),
            'dateTo': date_to.strftime("%d/%m/%Y"),
            'partner': PARTNER
        }

        r = requests.get(SEARCH_API, params=data)
        if r.status_code == 200:
            print('success!!!')
            results = r.json().get('data')
            print(len(results))

            for r in results:
                create_flight(r)


def check_flight(booking_token=None):
    response = {
        'empty': True
    }
    if booking_token is None:
        return response

    data = {
        'v': 2,
        'booking_token': booking_token,
        'bnum': 3,
        'pnum': 2
    }

    r = requests.get(CHECK_API, params=data)
    if r.status_code == 200:
        result = r.json()
        messages = []

        if result.get('price_change') == True:
            messages.append('Цена изменена')
        if result.get('flights_invalid') == True:
            messages.append('Данный перелет не валиден')

        response = {'messages': messages, 'status': 'ERR'}
        if not len(messages):
            response['status'] = 'OK'


    return response
