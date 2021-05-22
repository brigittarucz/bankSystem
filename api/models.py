from django.db import models

# API data object
# Currency reported to base USD (PATCH)
# /v1/latest 
# /v1/currency_name
class Currency(models.Model):
    currency_name = models.CharField(max_length=30, null=False)
    currency_code = models.CharField(max_length=3, null=False)
    currency_image = models.CharField(max_length=300, null=False)
    currency_symbol = models.CharField(max_length=3, null=False)
    currency_timestamp = models.IntegerField(null=False, default=0)
    currency_rate = models.DecimalField(decimal_places=10, max_digits=20, default=0)

    def __str__(self):
        return f"{self.currency_name} - {self.currency_code} - {self.currency_timestamp} - {self.currency_rate}"

    

# API data object
# Rates reported to base USD (POST)
# /v1/currency_name/historical/date_from/date_to
# /v1/convert/USD/currency_to/amount
class Rate(models.Model):
    rate_code = models.CharField(max_length=3, null=False)
    rate_timestamp = models.IntegerField(null=False, default=0)
    rate_value = models.DecimalField(decimal_places=10, max_digits=20, default=0)

    def __str__(self):
        return f"{self.rate_code} - {self.rate_timestamp} - {self.rate_value}"