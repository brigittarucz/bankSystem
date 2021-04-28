from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from django.http import HttpResponse
# from rest_framework.response import Response
from .models import Currency
from .serializers import CurrencySerializer

# Functions vs Class Based Views

class CurrencyList(generics.ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

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

