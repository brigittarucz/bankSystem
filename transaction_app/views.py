from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# from django import forms
from django.contrib.auth import authenticate, login

#Utilitie for random string
from django.utils.crypto import get_random_string

#Utilities for messages
from django.contrib import messages

from django.db import transaction
# from auth_app.models import Profile
from accounts_app_account.models import Account
from .models import Transaction






def index(request):
    # Dashboard/Page of transactions/loans
    return render(request, 'transaction_app/index.html')

#Transactions view
def transaction_view(request):
    user = request.user
    account = Account.objects.get(id=user.id)

    # @transaction.atomic
    # Logic to get the balance from the current usery
    context = {
        "account" : account,
            }

    if request.method == 'POST':
        balance_sender = account.account_balance
        receiver = request.POST['receiver']
        amount = request.POST['amount']
        amount = int(amount)
        if balance_sender >= amount:
            transaction = Transaction()
            unique_id = get_random_string(length=32)
            # Getting the account data from the receiver
            #should be the current session/user id.
            transaction.transaction_account_number_sender = account.account_number
            #should be autogenerate, check UUID
            transaction.transaction_id = unique_id
            transaction.transaction_account_number_receiver = receiver
            receiver_ =  Account.objects.get(account_number=receiver)
            transaction.transaction_amount = amount
            transaction.transaction_currency = 'DKK'
            balance_sender = balance_sender - amount
            account.account_balance = balance_sender
            receiver_.account_balance = receiver_.account_balance + amount
            
            receiver_.save()
            account.save()
            transaction.save()
            print('the balance of the sender is: ', balance_sender)
            return HttpResponseRedirect('/transaction/confirmation/')
        else: 
            #Should print some error message in the frontend, maybe with the if operator
            print("you don't have enough money")

    return render(request, 'transaction_app/transaction.html', context)





def transactions_view(request):
    user = request.user
    account = Account.objects.get(id=user.id)
    transactions = Transaction.objects.filter(transaction_account_number_sender=account.account_number)
    current_user = request.user
    print(current_user) 
    context = { 'transactions' : transactions}
    return render(request, 'transaction_app/transactions.html', context )


def confirmation_view(request):
    # transaction = Transaction()
    user = request.user
    account = Account.objects.get(id=user.id)
    user_transactions = Transaction.objects.filter(transaction_account_number_sender = account.account_number )
    latest_transaction = user_transactions.latest('transaction_date')
    context = { "latest_transaction" : latest_transaction}
    return render(request, 'transaction_app/confirmation.html', context)