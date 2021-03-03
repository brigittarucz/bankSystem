from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
# Equivalent: from django.forms import ModelForm
from django import forms

class SignupForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_staff'
        ]

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]

def login(request):
    form = LoginForm(None)
    context = {
        'form': form
    }
    # First argument = request object
    # Second argument = template string
    # Third argument = data dictionary
    return render(request, 'auth_app/login.html', context)


def signup(request):
    form = SignupForm(None)
    context = {
        'form': form
    }
    return render(request, 'auth_app/signup.html', context)