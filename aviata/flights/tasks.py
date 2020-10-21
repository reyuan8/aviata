import datetime
import requests
from celery.task import periodic_task
from celery.schedules import crontab
from aviata.flights.consts import directions
from aviata.flights.models import Direction, Flight
from aviata.flights.utils import create_flight
from aviata.taskapp.celery import app


SEARCH_API = 'https://api.skypicker.com/flights'
CHECK_API = 'https://booking-api.skypicker.com/api/v0.1/check_flights?'
PARTNER = 'picky'


@app.task(bind=True, max_retries=4)
def task_2(cls, result):
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

    # flight = Flight.objects.create(**data)
    flight = Flight.objects.bulk_create(Flight(**data), ignore_conflicts=True)
    print(flight.id)


@app.task(bind=True, max_retries=4)
def task_1(cls):
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
                task_2.delay(r)


@periodic_task(run_every=crontab(minute=0, hour=0))
def load_flights():
    # runs every day at 00:00
    task_1.delay()
