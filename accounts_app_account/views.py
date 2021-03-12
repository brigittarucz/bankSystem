from django.shortcuts import render

from .models import Account 
from transaction_app.models import Transaction
from auth_app.models import Profile

def accounts_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    user_account = Account.objects.filter(account_user_fk=profile)
    context = {
        "user": user,
        "user_accounts": user_account,
    }
    return render(request, "accounts_app_account/account.html", context)





