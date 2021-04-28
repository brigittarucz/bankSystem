from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
# from django.http import HttpResponse
# from rest_framework.response import Response
from .models import Currency
from .serializers import CurrencySerializer

# @api_view(['GET'])
class CurrencyList(generics.ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class CurrencyDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (permissions.IsAuthenticated, )
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer