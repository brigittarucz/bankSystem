# from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
from .forms import SignupProfileForm, SignupUserForm, LoginForm
from django.contrib.auth.models import User
from .models import Profile
from django.db import transaction, DatabaseError
from django.contrib.auth.decorators import login_required
from accounts_app_account.models import Account

import random
import string

@login_required(login_url='/auth/login/')
def dashboard(request):
    return render(request, 'auth_app/dashboard.html')

def logout(request):
    # Calls also flush() which removes session data
    logoutUser(request)
    return HttpResponseRedirect(reverse('auth_app:login'))

def login(request):
    form = LoginForm(None)
    # Uses context to pass data
    # form.as_p renders as paragraphs 
    context = {
        'form': form
    }
    
    # admin3 and test 
    if request.method == "POST":
        loginForm = LoginForm(data=request.POST)
        if loginForm.is_valid():
            userObject = authenticate(request, username=request.POST['username'], password=request.POST['password']) 
            if userObject:
                loginUser(request, userObject)
                # Todo: get user rank
                # context = {
                #     'username': request.POST['username']
                # }
                # First / cleans up the URL clean following the paths in urls.py
                # return render(request, 'auth_app/dashboard.html', context)

                # The previous does not change route, we pass context in session
                request.session['username'] = request.POST['username']
                return HttpResponseRedirect(reverse('auth_app:dashboard'))
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
        signupForm = SignupUserForm(request.POST)
        if signupForm.is_valid():
            # No password verification because that is provided out of the box
            profileForm = SignupProfileForm(request.POST)
            if profileForm.is_valid():
                post_username = request.POST['username']
                post_fname = request.POST['first_name']
                post_lname = request.POST['last_name']
                post_email = request.POST['email']
                post_password = request.POST['password1']
                post_phone = request.POST['customer_phone_number']
                # MultiValueDict's get fetches a value and provides a default
                post_mfe = request.POST.get('customer_mfe', False)
                post_mfe = True if post_mfe == 'on' else False
                # post_mfe = True if request.POST['customer_mfe'] == 'on' else False

                exception = True

                # Transactions: https://django.cowhite.com/blog/customizing-user-details-user-models-and-authentication/
                try:
                    with transaction.atomic():
                        # create_user() hashes the password
                        user = User.objects.create_user(email = post_email, 
                                                        username = post_username, 
                                                        password = post_password, 
                                                        first_name = post_fname, 
                                                        last_name = post_lname)
                        # create() does not hash 
                        profile = Profile.objects.create(user = user, 
                                                customer_rank = 'bronze',
                                                customer_phone_number = post_phone,
                                                customer_token = '123token', 
                                                customer_mfe = post_mfe, 
                                                customer_can_loan = False)
                        
                        letters = string.digits
                        value = ( ''.join(random.choice(letters) for i in range(20)) )
                        account = Account.objects.create(
                                                account_user_fk=user.id,
                                                account_number=value,
                                                account_balance=0.00

                        )
                        # Test exception:
                        # if exception:
                        #     raise exception
                except DatabaseError:
                    print("Transaction failed")
                    pass
                
                # Todo: both login + signup pass session ID
                # If it succeeds
                context = {
                    'username': post_username
                }

                return render(request, 'auth_app/dashboard.html', context)
            
            else: 
                context = {
                    'signup_user': signup_user,
                    'profile_user': profileForm
                }
        else:
            context = {
                'signup_user': signupForm,
                'profile_user': profile_user
            }

    return render(request, 'auth_app/signup.html', context)

# Migrations issues:
# https://stackoverflow.com/questions/34548768/django-no-such-table-exception

# Todo: admin view models enabled
# Todo: check routing for logging in url