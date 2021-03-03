from django.contrib.auth.models import User
from django.db import models

class Customer(models.Model):
    RANK_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze')
    ]

    # user = User.objects.create_user('username', first_name='positional-arg', last_name='positional-arg')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_rank = models.CharField(max_length=10, choices=RANK_CHOICES)
    customer_phone_number = models.CharField(max_length=20)
    customer_token = models.CharField(max_length=256)
    # Multi factor enabled
    customer_mfe = models.BooleanField(blank=False)
    customer_can_loan = models.BooleanField(blank=False)

    # Converts Python obj into strings
    def __str__(self):
        return f"{self.user}"


