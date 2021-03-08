from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from auth_app.models import Profile
from accounts_app_account.models import Account
from django.contrib.auth.forms import UserCreationForm
from django import forms

# SignupUserForm inherits from UserCreationForm
class SignupUserForm(UserCreationForm):
    # As UserCreationForm provides only 3 params 
    # username, password1, password2 we create the others
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)

    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',
    ]

def main(request):
    context = {
        'customers': Profile.objects.all(),
        'accounts': Account.objects.all(),
    }

    print(context)

    return render(request, 'employee_app/get_customers_accounts.html', context)


def edit(request):
    context = {
        'createCustomer': SignupUserForm
    }

    return render(request, 'employee_app/edit_customers_accounts.html', context)

def create(request):
    context = {
        'createCustomer': SignupUserForm
    }

    return render(request, 'employee_app/create_customers_accounts.html', context)