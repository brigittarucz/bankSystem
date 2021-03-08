from django.urls import path
from . import views

app_name = 'employee_app'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('edit/<int:customer_id>/', views.edit, name='edit'),
    path('create/' , views.create, name='create'),
]



