from rest_framework import serializers
from .models import Currency, Rate

# Serializers convert model instances to Python dictionaries
# so they can be rendered in various API formats (e.g JSON)

class CurrencySerializer(serializers.ModelSerializer):
   class Meta:
      model = Currency
      fields = ('currency_name', 'currency_code', 'currency_image', 'currency_symbol', 'currency_timestamp', 'currency_rate')

class SymbolSerializer(serializers.ModelSerializer):
   class Meta:
      model = Currency
      fields = ('currency_name', 'currency_code', 'currency_symbol')

class RateSerializer(serializers.ModelSerializer):
   class Meta:
      model = Rate
      fields = ('rate_code', 'rate_timestamp', 'rate_value')
