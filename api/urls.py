from django.urls import path
from .views import CurrencyList, api_currency_detail

app_name = 'api'

urlpatterns = [
    path('latest/', CurrencyList.as_view()),
    path('latest/<str:currency_code>/', api_currency_detail, name="detail"),
]