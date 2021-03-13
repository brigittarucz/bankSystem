from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from auth_app.models import Profile
from accounts_app_account.models import Account
from django.contrib.auth.models import User
from django.db import transaction, DatabaseError
from .forms import CustomerFormCreateValidation, CustomerFormEditValidation, AccountFormCreateValidation
from transaction_app.models import Loan, Transaction
from django.contrib.admin.views.decorators import staff_member_required

import random
import string

@staff_member_required
def overview_customers(request):
    # Todo: Add transactions and payments
    # Todo: Add in base.html employee navigation
    context = {
        'customers': Profile.objects.all(),
        'accounts': Account.objects.all(),
    }

    # print(context)

    return render(request, 'employee_app/overview_customers.html', context)

@staff_member_required
def edit_customer(request, customer_id):
    customer_id = int(customer_id)
    context = {}
    try:
        customer = Profile.objects.get(id=customer_id)
    except Profile.DoesNotExist:
            # Todo: Add context with errors
            return overview_customers(request)

    # GET method for populating form
    if request.method == 'GET':
        context = {
            'customer': customer
        }

    # POST method for editing user
    if request.method == 'POST':
        customerForm = CustomerFormEditValidation(request.POST)
        if customerForm.is_valid():
            # Todo: Check if passwords match
            customer.user.email = request.POST['email']

            customer.customer_rank = request.POST['customer_rank']
            customer.customer_phone_number = request.POST['customer_phone_number']
            post_loan = request.POST.get('customer_can_loan', False)
            post_loan = True if post_loan == 'on' else False
            customer.customer_can_loan = post_loan
            
            try:
                with transaction.atomic():
                    customer.save()
                
                context = {
                    'customers': Profile.objects.all(),
                    'accounts': Account.objects.all(),
                    'edited_user': customer
                }

                return render(request, 'employee_app/overview_customers.html', context)
            except DatabaseError:
                # Todo: print error message
                return render(request, 'employee_app/create_customer.html')
        else:
            context = {
                'customer': customer,
                'customerFormErrors': customerForm
            }      
            

    return render(request, 'employee_app/edit_customer.html', context)

@staff_member_required
def create_customer(request):

    context = {}

    if request.method == "POST":
        customerForm = CustomerFormCreateValidation(request.POST)
        if customerForm.is_valid():
            print()
            # Todo: Check if form valid & form fields not empty
            # Todo: Validate against existing username in DB
            post_username = request.POST['username']
            post_fname = request.POST['first_name'] 
            post_lname = request.POST['last_name']
            # Todo: Check if passwords match
            post_email = request.POST['email']
            post_password = request.POST['password1']
            post_rank = request.POST['customer_rank']
            post_phone = request.POST['customer_phone_number']
            post_loan = request.POST.get('customer_can_loan', False)
            post_loan = True if post_loan == 'on' else False
            # post_loan = True if request.POST['customer_can_loan'] == 'on' else False

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
                                                    customer_rank = post_rank,
                                                    customer_phone_number = post_phone,
                                                    customer_token = '123token', 
                                                    customer_mfe = False, 
                                                    customer_can_loan = post_loan)
                # Test exception:
                # if exception:
                #     raise exception

                # Todo: render overview customers with context     
                context = {
                    'customers': Profile.objects.all(),
                    'accounts': Account.objects.all(),
                    'new_user': user
                }

                return render(request, 'employee_app/overview_customers.html', context)
            except DatabaseError:
                # Todo: print error message
                return render(request, 'employee_app/create_customer.html')
                
                # print(DatabaseError)
                # pass
        else:
            context = {
                'customerFormErrors': customerForm
            }

    return render(request, 'employee_app/create_customer.html', context)

@staff_member_required
def edit_customer_account(request, customer_id, customer_account_id):
    customer_id = int(customer_id)
    account_id = int(customer_account_id)
    # Todo: add payments
    context = {}

    # myLoanUsername
    # mypassword123
    try:
        customer = Profile.objects.get(id=customer_id)
        account = Account.objects.get(id=account_id)
        loans = Loan.objects.filter(loan_account_fk=customer)
        transactions = Transaction.objects.filter(transaction_user_account_fk=account)
    # Multiple exceptions are handled in a tuple
    except (Profile.DoesNotExist, Account.DoesNotExist):
        # Todo: Add context with errors
         return overview_customers(request)

    # GET method for populating form
    if request.method == 'GET':
        # Lambda is the anonymous fc equiv. in python
        # List() is necessary due to list comprehensions and python3.x
        context = {
            'customer': customer,
            'account': account,
            'transactions': transactions,
            'loansFinished': list(filter(lambda x: x.is_ongoing() == 0, loans)),
            'loansOngoing': list(filter(lambda x: x.is_ongoing() == 1, loans))
        }

    # POST method for modifying balance
    if request.method == 'POST':
        post_balance = request.POST['account_balance']

        # Todo: validate post_balance
        account.account_balance = post_balance
        account.save()

        context = {
            'customers': Profile.objects.all(),
            'accounts': Account.objects.all(),
            'edited_account': account
        }

        return render(request, 'employee_app/overview_customers.html', context)

    return render(request, 'employee_app/edit_customer_account.html', context)

@staff_member_required
def create_customer_account(request):
    if request.method == 'GET':
        context = {
            'customers': Profile.objects.all()
        }

    if request.method == 'POST':
        try:
            customer = Profile.objects.get(id=request.POST['account_user_fk'])
            accountForm = AccountFormCreateValidation(request.POST)
            print(accountForm)
            if accountForm.is_valid():
                try:
                    letters = string.digits
                    value = ( ''.join(random.choice(letters) for i in range(20)) )
                    account = Account.objects.create(
                                    account_user_fk=customer,
                                    account_number=value,
                                    account_balance=request.POST['account_balance']              
                    )
                    return overview_customers(request)
                except DatabaseError:
                    # Todo: Print error message
                    return render(request, 'employee_app/create_customer_account.html', context)
        except Profile.DoesNotExist:
            # Todo: Print error message
            return render(request, 'employee_app/create_customer_account.html', context)   

    return render(request, 'employee_app/create_customer_account.html', context)