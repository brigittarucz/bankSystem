from django.urls import path
from .views import CurrencyList, CurrencyDetail

app_name = 'api'

urlpatterns = [
    path('latest/', CurrencyList.as_view()),
    path('<str:currency_name>/', CurrencyDetail.as_view()),
]