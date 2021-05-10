from django.db import models
from auth_app.models import Profile
# Create your models here.
class Account(models.Model):
    account_user_fk = models.ForeignKey(Profile, on_delete=models.PROTECT)
    account_number = models.CharField(max_length=20, null=False)
    account_balance = models.DecimalField(decimal_places=2,max_digits=7, default=0)

    def __str__(self):
        # Returning string of the id
        return f"Number {self.account_number} - Name:{self.account_user_fk} - Balance: {self.account_balance}"

    @classmethod
    def create_account(self, profile, value, balance):
        account = Account.objects.create(account_user_fk=profile,
                                         account_number=value,
                                         account_balance=balance)

        account.save()
        return account