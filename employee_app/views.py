from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from auth_app.models import Profile
from accounts_app_account.models import Account
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignupUserForm(UserCreationForm):
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


def edit(request, customer_id):
    customer_id = int(customer_id)

    if request.method == 'GET':
        try:
            customer = Profile.objects.filter(id=customer_id).values()[0]
        except Profile.DoesNotExist:
            return render(request, 'employee_app/get_customers_accounts.html')

        data = {''}

        populatedSignupUserForm = SignupUserForm(instance = customer)

        context = {
            'createCustomer': populatedSignupUserForm
        }

    print(customer)

    return render(request, 'employee_app/edit_customers_accounts.html', context)

def create(request):
    context = {
        'createCustomer': SignupUserForm
    }

    return render(request, 'employee_app/create_customers_accounts.html', context)