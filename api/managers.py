# managers.py
from django.db import models
from django.db.models import Manager

class RateManager(Manager):
    def get_specific_rates(self, rate_code):
        return self.filter(rate_code=rate_code)

