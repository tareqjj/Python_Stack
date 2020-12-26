import requests
from currency_exchange_app.models import Rate


def _get_rate_json():
    url = 'http://data.fixer.io/api/latest'
    access_key = '4405fe87f8ab4f75dc9765319b17f661'
    symbols = 'USD,JOD,GBP,JPY,ILS'

    r = requests.get('{0}?access_key={1}&symbols={2}'.format(
        url,
        access_key,
        symbols))

    try:
        r.raise_for_status()
        return r.json()
    except:
        return None


def update_forecast():
    json = _get_rate_json()
    if json is not None:
        try:
            new_rate = Rate()

            # open weather map gives temps in Kelvin. We want celsius.
            new_rate.timestamp = json['timestamp']
            new_rate.date = json['date']
            new_rate.USD = json['rates']['USD']
            new_rate.JOD = json['rates']['JOD']
            new_rate.GBP = json['rates']['GBP']
            new_rate.JPY = json['rates']['JPY']
            new_rate.ILS = json['rates']['ILS']
            new_rate.save()
            print("saving...\n" + new_rate)
        except:
            pass