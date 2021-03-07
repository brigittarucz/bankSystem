from django.db import models

# Create your models here.
class Account(models.Model):
    account_user_fk = models.IntegerField()
    account_number = models.CharField(max_length=20, null=False)
    account_balance = models.DecimalField(decimal_places=2,max_digits=7, default=0)
 

    def __str__(self):
        # Returning string of the id
        return f"Number {self.account_number} - Name:{self.account_user_fk}"

