from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from auth_app.models import Profile
from accounts_app_account.models import Account

def main(request):
    context = {
        'customers': Profile.objects.all(),
        'accounts': Account.objects.all(),
    }

    print(context)

    return render(request, 'employee_app/get_customers_accounts.html', context)
