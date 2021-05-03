from celery import shared_task
from api.models import Currency
import requests

CURRENCY_API = 'http://api.openweathermap.org/data/2.5/weather?q=London&appid=3c43fac79a2cc3e14edecaf8911f8e2c'
POST_API = 'http://127.0.0.1:8000/api/v1/create/'

GET_CURRENCY_API_EX = 'https://api.ratesapi.io/api/latest?base=USD'
UPDATE_CURRENCY_API_IN = 'http://127.0.0.1:8000/api/v1/update/'

# Lets us create tasks without having concrete app
@shared_task()
def get_currency(seconds):
    
    r = requests.get(CURRENCY_API)
    print(r.json())

@shared_task()
def post_rate():

    payload = {
        'rate_code': 1
    }

    r = requests.post(POST_API, data=payload)

@shared_task()
def update_rates():
    # 1. Get current rates from api
    currencies = Currency.objects.all()
    r = requests.get(GET_CURRENCY_API_EX)
    currencyObject = r.json()
    print(currencyObject['rates'])
    
    if r.status_code == 200:
        for currency in currencies:
            currency_code = currency.currency_code
            # 2. Get existent DB elems
            # 3. Patch them one by one

            Currency.objects.filter(currency_code=currency_code).update(currency_rate=currencyObject['rates'][currency_code])
            


# get_currency.delay(4)
# get_currency(2)
# python3 -m celery -A banking_system worker -l info
# python3 -m celery -A banking_system beat -l info 