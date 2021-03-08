from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from auth_app.models import Profile
from accounts_app_account.models import Account
from django.contrib.auth.models import User
from django.db import transaction, DatabaseError

def overview_customers(request):
    # Todo: Add transactions and payments
    # Todo: Add in base.html employee navigation
    context = {
        'customers': Profile.objects.all(),
        'accounts': Account.objects.all(),
    }

    print(context)

    return render(request, 'employee_app/overview_customers.html', context)


def edit_customer(request, customer_id):
    customer_id = int(customer_id)

    if request.method == 'GET':
        try:
            customer = Profile.objects.get(id=customer_id)
        except Profile.DoesNotExist:
            # Todo: Add context with errors
            return render(request, 'employee_app/overview_customers.html')

    return render(request, 'employee_app/edit_customer.html')

def create_customer(request):

    if request.method == "POST":
        # Todo: Check if form valid
        post_username = request.POST['username']
        post_fname = request.POST['first_name'] 
        post_lname = request.POST['last_name']
        # Todo: Check if passwords match
        post_email = request.POST['email']
        post_password = request.POST['password1']
        post_rank = request.POST['customer_rank']
        post_phone = request.POST['customer_phone_number']

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
                                                customer_can_loan = False)
        # Test exception:
            # if exception:
            #     raise exception
        # Todo: render overview customers with context     
        except DatabaseError:
            print(DatabaseError)
            pass

    return render(request, 'employee_app/create_customer.html')

def edit_customer_account(request, customer_account_id):
    return render("Works")

def create_customer_account(request):
    return render("Works")