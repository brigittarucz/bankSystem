from django.shortcuts import render

from .models import Account 
from transaction_app.models import Transaction
from auth_app.models import Profile

def accounts_view(request):
    user = request.user
    user_account = Account.objects.filter(account_user_fk=user.id)
    customer = Profile.objects.get(user=user)
    context = {
        "user": user,
        "user_accounts": user_account,
        "customer": customer
    }
    print(customer)
    return render(request, "accounts_app_account/account.html", context)





