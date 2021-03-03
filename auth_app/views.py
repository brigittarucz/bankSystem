from django.shortcuts import render
from django.http import HttpResponse

from .models import Customer

def login(request):
    # users = Customer.object.all()

    # First argument = request object
    # Second argument = template string
    # Third argument = data dictionary
    return render(request, 'auth_app/login.html', {})
