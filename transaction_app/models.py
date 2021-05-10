from django.db import models
from django.core.validators import MinValueValidator
from accounts_app_account.models import Account
from auth_app.models import Profile

#Utilitie for random string
from django.utils.crypto import get_random_string

class Transaction(models.Model):
    # account = models.ForeignKey(Account, on_delete=models.PROTECT   )
    transaction_user_account_fk = models.ForeignKey(Account, on_delete=models.PROTECT)
    transaction_account_number_sender = models.CharField(max_length=20, null=False)
    transaction_account_number_receiver = models.CharField(max_length=20, null=False)
    # Maybe we can use UUUIDField
    transaction_id = models.CharField(max_length=20)
    transaction_amount = models.DecimalField(decimal_places=2,max_digits=7, validators=[MinValueValidator(5.00)])
    transaction_currency = models.CharField(max_length=3)
    transaction_date = models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        # Returning string of the id
        return f"{self.transaction_id} - {self.transaction_date} - {self.transaction_account_number_sender}"

    @classmethod
    def create_transaction(self, account, account_sender, account_receiver, amount):
        transaction = Transaction.objects.create(transaction_user_account_fk=account,
                                                 transaction_account_number_sender=account_sender,
                                                 transaction_account_number_receiver=account_receiver,
                                                 transaction_id = get_random_string(length=20),  
                                                 transaction_amount=amount,
                                                 transaction_currency='DKK')

        return transaction

# Bug found: If I want to pay more money than I have to on my loan
# Bug found: Account balanace can go negative ( guess it's for testing purposes )

# What is loan_remain? The amount paid?
class Loan(models.Model):

    loan_account_fk = models.ForeignKey(Profile, on_delete=models.PROTECT)
    loan_id = models.CharField(max_length=20, null=False)
    loan_description =  models.CharField(max_length=20, null=False)
    loan_amount = models.DecimalField(decimal_places=2,max_digits=7, validators=[MinValueValidator(5.00)])
    loan_date = models.DateTimeField(auto_now_add=True)
    loan_remain = models.DecimalField(decimal_places=2,max_digits=7, validators=[MinValueValidator(5.00)])

    def is_ongoing(self):
        return 1 if self.loan_amount - (-self.loan_remain) > 0 else 0

    def __str__(self):
        # Returning string of the id
        return f"{self.loan_account_fk} - {self.loan_description} - {self.loan_amount} - {self.loan_date}"

    @classmethod
    def create_loan(self, profile, description, amount, remained):
        loan = Loan.objects.create(loan_account_fk = profile,
                                   loan_id=get_random_string(length=20),
                                   loan_description=description,
                                   loan_amount=amount,
                                   loan_remain=remained)

        return loan