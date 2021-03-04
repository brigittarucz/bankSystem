# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as loginMethod, logout as logoutMethod
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Equivalent: from django.forms import ModelForm
from django import forms

# SignupUserForm inherits from UserCreationForm
class SignupUserForm(UserCreationForm):
    # As UserCreationForm provides only 3 params 
    # username, password1, password2 we get the others from the User model
    
    # The Meta class has two functions:
    # 1. Indicate which model we are using
    # 2. Show the fields we want to include in our final form
    class Meta:
        model = User 
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
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
    form = SignupUserForm(None)
    context = {
        'form': form
    }
    return render(request, 'auth_app/signup.html', context)