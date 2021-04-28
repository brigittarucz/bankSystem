from rest_framework import serializers
from .models import Currency

# Serializers convert model instances to Python dictionaries
# so they can be rendered in various API formats (e.g JSON)

class CurrencySerializer(serializers.ModelSerializer):
   class Meta:
      model = Currency
      fields = ('currency_name', 'currency_code')