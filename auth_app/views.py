# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as loginMethod, logout as logoutMethod
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Equivalent: from django.forms import ModelForm
from django import forms
from .models import Profile


# Future Todo: Move the forms in a separate forms.py file 
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

class SignupProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'customer_rank'
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
    
    # admin3
    # test
    if request.method == "POST":
        userObject = authenticate(request, username=request.POST['username'], password=request.POST['password']) 
        if userObject:
            loginMethod(request, userObject)
            context = {
                'username': 'John'
            }
            # First / cleans up the URL clean following the paths in urls.py
            return render(request, 'auth_app/dashboard.html', context)
        else:
            return render(request, 'auth_app/login.html', context)

    # First argument = request object
    # Second argument = template string
    # Third argument = data dictionary
    return render(request, 'auth_app/login.html', context)


def signup(request):
    # https://stackoverflow.com/questions/59133456/how-to-add-2-models-in-a-registration-form-in-django
    signup_user = SignupUserForm()
    profile_user = SignupProfileForm()
    context = {
        'signup_user': signup_user,
        'profile_user': profile_user
    }

    if request.method == "POST":
        # This:
        # print(request.POST)
        # Prints this:
        # <QueryDict: {'csrfmiddlewaretoken': ['A0390Q8p7lzY50KSCbWpfs1hW7T40G8I5zhYYliyyHbAd1oaSTq9gkSlYHxEHCh0'], 'username': ['root'], 'first_name': [''], 'last_name': [''], 'email': [''], 'password1': ['v!rbeK9kHj6uLTh'], 'password2': ['v!rbeK9kHj6uLTh'], 'customer_rank': ['gold']}>
        # signup_user_post = SignupUserForm(request.POST) OR
        username_post = request.POST['username']
        fname_post = request.POST['first_name']
        lname_post = request.POST['last_name']
        email_post = request.POST['email']
        password_post = request.POST['password1']
        # Python's ternary operator
        is_staff_post = True if request.POST['is_staff'] == 'on' else False
        customer_rank_post = request.POST['customer_rank']
        # create_user() hashes the password
        user = User.objects.create_user(email = email_post, username = username_post, password = password_post, is_staff = is_staff_post)
        # create() does not hash 
        profile = Profile.objects.create(user = user, customer_rank = customer_rank_post, customer_mfe = False, customer_can_loan = False)
        # Todo: check for password
        # Todo: correct fields
        # Todo: add transactions
        # Todo: verify validity
        print(user)
        print(profile)
        # Transactions: https://django.cowhite.com/blog/customizing-user-details-user-models-and-authentication/





    return render(request, 'auth_app/signup.html', context)

# Migrations issues:
# https://stackoverflow.com/questions/34548768/django-no-such-table-exception