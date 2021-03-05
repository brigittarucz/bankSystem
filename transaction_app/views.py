from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import forms
from django.db import transaction

from .models import Transaction



class transactionForm(forms.Form):
    account_receiver = forms.CharField(label='Account Receiver', max_length=100)
    ammount = forms.DecimalField(label='How much money would you like send?')



def transaction_view(request):


    # @transaction.atomic
    # Logic to get the balance from the current usery
    
    if request.method == 'POST':
        form = transactionForm(request.POST)
        # amount = request.POST['amount']
        transaction = Transaction()
        # transaction.transaction_amount = ammount

        if form.is_valid():
            return HttpResponseRedirect('/confirmation/')
    
    # if request.accounts_app.balance >= 

    else:
        form = transactionForm()

    
    context = {
        "form" : transactionForm
            }

    
    return render(request, 'transaction_app/transaction.html', context)


# def get_transactions(self):
#     return Transaction.objects.filter(receiver=self.kwargs['pk'])



def transactions_view(request):
     
    # transaction = Transaction.filter(transaction_account_number_sender = account.id)
    # context = {
    #     'transactions' : transactions
    # }
    return render(request, 'transaction_app/transactions.html', {} )


def confirmation_view(request):
    return render(request, 'transaction_app/confirmation.html', {})