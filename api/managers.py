# managers.py
from django.db import models
from django.db.models import Manager

# https://docs.djangoproject.com/en/3.2/topics/db/managers/
class RateManager(Manager):
    def get_specific_rate(self, rate_code):
        return self.filter(rate_code=rate_code)

    def get_range_rates(self, rate_from, rate_to):
        return self.filter(rate_timestamp__range=(rate_from, rate_to))
