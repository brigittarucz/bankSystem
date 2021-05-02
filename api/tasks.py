from celery import shared_task
import requests

CURRENCY_API = 'http://api.openweathermap.org/data/2.5/weather?q=London&appid=3c43fac79a2cc3e14edecaf8911f8e2c'

# Lets us create tasks without having concrete app
@shared_task()
def get_currency(seconds):
    
    r = requests.get(CURRENCY_API)
    print(r.json())

# get_currency.delay(4)
# get_currency(2)
# python3 -m celery -A banking_system worker -l info
# python3 -m celery -A banking_system beat -l info 