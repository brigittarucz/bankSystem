from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from django.http import HttpResponse
# from rest_framework.response import Response
from .models import Currency, Rate
from .serializers import CurrencySerializer, SymbolSerializer, RateSerializer
from datetime import datetime
from api.models import Rate

class CurrencyList(generics.ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class SymbolList(generics.ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = Currency.objects.all()
    serializer_class = SymbolSerializer

class RateList(generics.ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

# GET request is allowed with the view
@api_view(['GET'])
def api_currency_detail(request, currency_code):

    try:
        currency_detail = Currency.objects.get(currency_code=currency_code)
        print(currency_detail)
    except Currency.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CurrencySerializer(currency_detail)
    return Response(serializer.data)

@api_view(['GET'])
def api_rate(request, rate_code):
    
    currency_rates = Rate.objects.filter(rate_code=rate_code)
    
    if not currency_rates:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Filter returns queryset - does not throw an error if empty
    # Get returns object
    # many = True is for filter
    serializer = RateSerializer(currency_rates, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_rate_historical_from(request, rate_code, rate_from):
    now = datetime.now()
    rate_to = datetime.timestamp(now)

    currency_historical = Rate.objects.filter(rate_timestamp__range=(rate_from, rate_to))
    
    if not currency_historical:
        return Response(status=status.HTTP_404_NOT_FOUND)

    currency_historical_code = currency_historical.filter(rate_code=rate_code)
    
    serializer = RateSerializer(currency_historical_code, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_rate_historical_range(request, rate_code, rate_from, rate_to):

    currency_historical = Rate.objects.filter(rate_timestamp__range=(rate_from, rate_to))
    if not currency_historical:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    currency_historical_code = currency_historical.filter(rate_code=rate_code)
    
    serializer = RateSerializer(currency_historical_code, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_convert(request, rate_code_from, rate_code_to, amount):
    # EUR/USD ÷ CAD/USD = EUR/CAD

    # Todo: handle USD case
    try:
        currency_from = Currency.objects.get(currency_code=rate_code_from)
    except Currency.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        currency_to = Currency.objects.get(currency_code=rate_code_to)
    except Currency.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # 1CAD = conversion_rate * 1 EUR
    # 1EUR = 1 / conversion_rate CAD
    conversion_rate_to = currency_from.currency_rate / currency_to.currency_rate
    conversion_rate_from = 1 / conversion_rate_to
    result = conversion_rate_from*amount

    print(result)

# Update current data
@api_view(['PATCH'])
def api_currency_detail_patch(request, currency_code):

    try:
        currency_detail = Currency.objects.get(currency_code=currency_code)
        print(currency_detail)
    except Currency.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = CurrencySerializer(currency_detail, data=request.data)
        # Data is similar to context for serializers
        data = {}
        # When updating something a serializer is very similar to a form
        if serializer.is_valid():
            serializer.save()
            data["success"] = "Update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def api_rate_historical_post(request):
    print("Here")
    now = datetime.now()
    rate_now = datetime.timestamp(now)

    rate = Rate(rate_code='dja', rate_timestamp=rate_now, rate_value=1)

    if request.method == 'POST':
        serializer = RateSerializer(rate, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update historical data