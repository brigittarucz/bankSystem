from django.contrib import admin

# Register your models here.

from transaction_app.models import Transaction
from transaction_app.models import Loan

admin.site.register(Transaction)
admin.site.register(Loan)