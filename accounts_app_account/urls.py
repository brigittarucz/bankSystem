from django.urls import path
from . import views

app_name = 'accounts_app_account'

urlpatterns = [
    path('', views.accounts_view, name='index'),
]