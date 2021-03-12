from django.urls import path
from . import views

app_name = 'employee_app'

urlpatterns = [
    path('overview_customers/', views.overview_customers, name='overview_customers'),
    path('edit_customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('edit_customer_account/<int:customer_id>/<int:customer_account_id>/' , views.edit_customer_account, name='edit_customer_account'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('create_customer_account/', views.create_customer_account, name='create_customer_account')
]



