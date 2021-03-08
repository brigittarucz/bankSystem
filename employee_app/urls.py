from django.urls import path
from . import views

app_name = 'employee_app'

urlpatterns = [
    path('employee/', views.employee, name='employee'),
]