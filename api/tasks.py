from celery import shared_task
from api.models import Currency, Rate
from datetime import datetime, timedelta
import requests

# CURRENCY_API= 'https://api.ratesapi.io/api/latest?base=USD'
CURRENCY_API= 'https://exchange-rates.abstractapi.com/v1/live/?api_key=d7c6b70553064c90ab1d0a893593021f&base=USD'
CURRENCY_API_HISTORICAL = 'https://exchange-rates.abstractapi.com/v1/live/?api_key=d7c6b70553064c90ab1d0a893593021f&base=USD&date='

# Lets us create tasks without having concrete app
@shared_task(max_retried=3)
def update_rates():
    # 0. Create array and delete all rates
    rates = ['DKK', 'GBP', 'HUF', 'RON', 'NOK', 'SEK', 'JPY', 'RUB', 'INR']

    Rate.objects.all().delete()

    # 1. Generate dates for each one of the past 15 days
    todayObj = datetime.today()

    for day in range(1, 15):
      
        dateObj = todayObj - timedelta(days=day)
        
        # 2. In a loop for each date, make a request 
        r = requests.get(CURRENCY_API_HISTORICAL + dateObj.strftime('%Y-%m-%d'))
        currencyObject = r.json()
        print(r.json())

        if r.status_code == 200:

            # 3. Create new object for each rate
            for rate in rates:
                newRate = Rate(rate_code=rate, 
                            rate_timestamp=int(datetime.timestamp(dateObj)), 
                            rate_value=currencyObject['exchange_rates'][rate])

                # 4. Save new obj to db
                newRate.save()


@shared_task(max_retries=3)
def update_currency_rates():
    # 1. Get current rates from api
    currencies = Currency.objects.all()
    r = requests.get(CURRENCY_API)
    currencyObject = r.json()
    print(currencyObject)
    
    if r.status_code == 200:
        for currency in currencies:
            currency_code = currency.currency_code
            # 2. Get existent DB elems
            # 3. Patch them one by one
            if currency_code != 'USD':
                Currency.objects.filter(currency_code=currency_code).update(currency_timestamp=currencyObject['last_updated'])
                Currency.objects.filter(currency_code=currency_code).update(currency_rate=currencyObject['exchange_rates'][currency_code])
            


# get_currency.delay(4)
# get_currency(2)
# python3 -m celery -A banking_system worker -l info
# python3 -m celery -A banking_system beat -l info 

# To update make sure you run Docker and the command below in the terminal:
# docker run -d -p 5672:5672 rabbitmq 
# docker run -d -p 6379:6379 redis
# python3 -m celery -A banking_system worker -l info -B 