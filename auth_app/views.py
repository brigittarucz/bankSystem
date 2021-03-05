# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from .forms import SignupProfileForm, SignupUserForm, LoginForm
from django.contrib.auth.models import User
from .models import Profile

def dashboard(request):
    return render(request, 'auth_app/dashboard.html')

def login(request):
    form = LoginForm(None)
    # Uses context to pass data
    # form.as_p renders as paragraphs 
    context = {
        'form': form
    }
    
    # admin3 and test 
    # superuser and validated1
    if request.method == "POST":
        loginForm = LoginForm(data=request.POST)
        if loginForm.is_valid():
            userObject = authenticate(request, username=request.POST['username'], password=request.POST['password']) 
            if userObject:
                loginUser(request, userObject)
                # Todo: get user rank
                context = {
                    'username': request.POST['username']
                }
                # First / cleans up the URL clean following the paths in urls.py
                return render(request, 'auth_app/dashboard.html', context)
            else:
                context = {
                    'form': form,
                    'error': 'Incorrect login data'
                }
                return render(request, 'auth_app/login.html', context)
        else:
            context = {
                'form': loginForm,
                'error': 'Invalid form'
            }

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
        signupForm = SignupUserForm(request.POST)
        if signupForm.is_valid():
            username_post = request.POST['username']
            fname_post = request.POST['first_name']
            lname_post = request.POST['last_name']
            email_post = request.POST['email']
            password_post = request.POST['password1']
            # Python's ternary operator
            is_staff_post = True if request.POST['is_staff'] == 'on' else False
            print(is_staff_post)
            customer_rank_post = request.POST['customer_rank']
            # create_user() hashes the password
            user = User.objects.create_user(email = email_post, username = username_post, password = password_post)
            # create() does not hash 
            profile = Profile.objects.create(user = user, customer_rank = customer_rank_post, customer_mfe = False, customer_can_loan = False)
            # Todo: check for password
            # Todo: correct fields
            # Todo: add transactions
            # Todo: verify validity
            print(user)
            print(profile)
            # Transactions: https://django.cowhite.com/blog/customizing-user-details-user-models-and-authentication/
        else:
            context = {
                'signup_user': signupForm,
                'profile_user': profile_user
            }




    return render(request, 'auth_app/signup.html', context)

# Migrations issues:
# https://stackoverflow.com/questions/34548768/django-no-such-table-exception