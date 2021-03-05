from django.db import models


# Customizations for the user
class Transaction(models.Model):
    transaction_account_number_sender = models.CharField(max_length=20, null=False)
    transaction_account_number_receiver = models.CharField(max_length=20, null=False)
    transaction_id = models.CharField(max_length=20)
    transaction_amount = models.DecimalField(decimal_places=2,max_digits=7)
    transaction_currency = models.CharField(max_length=3)
    transaction_date = models.DateTimeField()
    # # Multi factor enabled
 

    def __str__(self):
        # Returning self would get an infinite loop
        return f"{self.transaction_id}"

