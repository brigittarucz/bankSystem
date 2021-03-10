from django.db import models
from django.core.validators import MinValueValidator
from accounts_app_account.models import Account




class Transaction(models.Model):
    # account = models.ForeignKey(Account, on_delete=models.PROTECT   )

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


class Loan(models.Model):

    loan_account_fk = models.ForeignKey(Account, on_delete=models.PROTECT)
    loan_description =  models.CharField(max_length=20, null=False)
    loan_amount = models.DecimalField(decimal_places=2,max_digits=7, validators=[MinValueValidator(5.00)])
    loan_date = models.DateTimeField(auto_now_add=True)