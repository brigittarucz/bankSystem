from django.shortcuts import render

from .models import Account 
from transaction_app.models import Transaction


def accounts_view(request):
    user = request.user
    user_account = Account.objects.filter(account_user_fk=user.id)
    context = {
        "user": user,
        "user_accounts": user_account,
    }

    return render(request, "accounts_app_account/account.html", context)





