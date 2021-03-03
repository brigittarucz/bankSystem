# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as loginMethod, logout as logoutMethod
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
            'username',
            'password'
        ]

def dashboard(request):
    return render(request, 'auth_app/dashboard.html')

def login(request):
    form = LoginForm(None)
    # Uses context to pass data
    # form.as_p renders as paragraphs 
    context = {
        'form': form
    }
    
    # admin
    # test
    if request.method == "POST":
        userObject = authenticate(request, username=request.POST['username'], password=request.POST['password']) 
        if userObject:
            loginMethod(request, userObject)
            # First / cleans up the URL clean following the paths in urls.py
            return HttpResponseRedirect('/auth/dashboard/')
        else:
            return print("does not work")

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