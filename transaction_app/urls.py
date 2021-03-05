from django.urls import path
from . import views

app_name = 'transaction_app'

urlpatterns = [
    path('new/', views.transaction_view, name='transaction'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('confirmation/', views.confirmation_view, name='confirmation'),
]