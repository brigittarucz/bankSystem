from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
# from django import forms
from django.contrib.auth import authenticate, login

#Utilitie for random string
from django.utils.crypto import get_random_string

#Utilities for messages
from django.contrib import messages

from django.db import transaction 

from accounts_app_account.models import Account
from auth_app.models import Profile
from .models import Transaction
from .models import Loan




def index(request):
    # Dashboard/Page of transactions/loans
    
    
    return render(request, 'transaction_app/index.html')

#Transactions view
def transaction_view(request):
    user = request.user 
    profile = Profile.objects.get(user=user)
    accounts = Account.objects.filter(account_user_fk=profile)
    # @transaction.atomic
    # Logic to get the balance from the current usery
    context = {
        "accounts" : accounts,
            }

    if request.method == 'POST':
        account_sender = request.POST['account_number_sender']
        
        account_selected = Account.objects.get(account_number=account_sender)
        print(account_selected)
        receiver = request.POST['receiver']
        amount = request.POST['amount']
        amount = int(amount)
        if account_selected.account_balance >= amount:
            transaction = Transaction()
            unique_id = get_random_string(length=20)
            # Getting the account data from the receiver
            transaction.transaction_account_number_sender = account_selected.account_number
            #should be autogenerate, check UUID
            transaction.transaction_user_account_fk = account_selected    
            transaction.transaction_id = unique_id
            transaction.transaction_account_number_receiver = receiver
            receiver_ =  Account.objects.get(account_number=receiver)
            transaction.transaction_amount = amount
            transaction.transaction_currency = 'DKK'
            balance_sender = account_selected.account_balance - amount
            account_selected.account_balance = balance_sender
            receiver_.account_balance = receiver_.account_balance + amount
            
            receiver_.save()
            account_selected.save()
            transaction.save()
            print('the balance of the sender is: ', balance_sender)
            return HttpResponseRedirect('/transaction/confirmation/')
        else: 
            #Should print some error message in the frontend, maybe with the if operator
            print("you don't have enough money")

    return render(request, 'transaction_app/transaction.html', context)





def transactions_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    accounts = Account.objects.filter(account_user_fk=profile)
    arrayTransaction=[]
    for account in accounts:
        transactions = Transaction.objects.filter(transaction_user_account_fk=account).values()
        for transaction in transactions:
            arrayTransaction.append(transaction) 

    context = {
                "arrayTransaction" : arrayTransaction
            }   
    
    return render(request, 'transaction_app/transactions.html', context )

                
    

def confirmation_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    accounts = Account.objects.filter(account_user_fk=profile)
    for account in accounts:
        user_transactions = Transaction.objects.filter(transaction_user_account_fk=account)
        
    latest_transaction = user_transactions.latest('transaction_date')
    context = { "latest_transaction" : latest_transaction}
    return render(request, 'transaction_app/confirmation.html', context)





def loan_payment(request):
    user = request.user
    user = request.user
    profile = Profile.objects.get(user=user)
    accounts = Account.objects.filter(account_user_fk=profile)
    loan = Loan.objects.filter(loan_account_fk=profile).latest('loan_date')
    if request.method == "POST":
        amount = request.POST['amount']
        amount = int(amount)
        account_number = request.POST['account_number']
        selected_account = Account.objects.get(account_number=account_number)
        account_balance = selected_account.account_balance
        updated_balance = account_balance - amount
        account_balance = updated_balance
        selected_account.account_balance = account_balance

        loan_remain = loan.loan_remain
        updated_loan_remain = loan_remain - amount
        print(updated_loan_remain)
        loan.loan_remain = updated_loan_remain
        transaction = Transaction.objects.create(transaction_user_account_fk=selected_account,
                                                 transaction_account_number_sender=account_number,
                                                 transaction_account_number_receiver='BankingSystem Loan Payment',
                                                 transaction_id = get_random_string(length=20),  
                                                 transaction_amount=amount,
                                                 transaction_currency='DKK')
        if loan.loan_remain == 0:
            profile.customer_can_loan = True
        selected_account.save()
        transaction.save()
        profile.save()
        loan.save()

        return render(request, 'transaction_app/index.html')
        
    else:
        context = {
        'accounts':accounts,
        'loan': loan
        }
        return render(request, 'transaction_app/payment.html', context)

    





def loan_view(request):
    
    user = request.user
    profile = Profile.objects.get(user=user)
    accounts = Account.objects.filter(account_user_fk=profile)
    loan = Loan.objects.filter(loan_account_fk=profile).latest('loan_date')
    
        
        
    if request.method == 'POST':
        total_amount = request.POST['total_amount']
        profile.customer_can_loan = False
        print(profile.customer_can_loan)
        total_amount = int(total_amount)
        account_number = request.POST['account_number']
        loan_description = request.POST['loan_description']
        selected_account = Account.objects.get(account_number=account_number)
        selected_account.account_balance = selected_account.account_balance + total_amount
        # selected_account.account_balance = selected_account.accounts_balance + total_amount
         
        loan = Loan.objects.create(loan_account_fk = profile,
                                    loan_id=get_random_string(length=20),
                                    loan_description=loan_description,
                                    loan_amount=total_amount,
                                    loan_remain=total_amount
                                    )
        transaction = Transaction.objects.create(transaction_user_account_fk=selected_account,
                                                 transaction_account_number_sender='Bank Loan',
                                                 transaction_account_number_receiver=selected_account.account_number,
                                                 transaction_id = get_random_string(length=20),  
                                                 transaction_amount=total_amount,
                                                 transaction_currency='DKK')
        
        transaction.save()                                         
        selected_account.save()
        profile.save()
        context ={
            "profile": profile,
            "user": user,
            "accounts": accounts,
            "transaction": transaction,
                }
        print('the user has applied for a loan of = ', total_amount, account_number, loan_description)
        return render(request, 'transaction_app/confirmationLoan.html', context)
     
        

    else: 
        
        print('you are not allowed to apply for a Loan. Please contact us')
        
    context ={
        "profile": profile,
        "user": user,
        "accounts": accounts,
        "loan":loan
    }
    
    return render(request, 'transaction_app/loan.html', context)





