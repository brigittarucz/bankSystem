from django.contrib.auth.models import User
from django.db import models

# Customizations for the user
class Profile(models.Model):
    RANK_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze')
    ]

    # user = User.objects.create_user('username', first_name='positional-arg', last_name='positional-arg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_rank = models.CharField(max_length=10, choices=RANK_CHOICES, default='bronze')
    customer_phone_number = models.CharField(max_length=20)
    customer_token = models.CharField(max_length=256)
    # # Multi factor enabled
    customer_mfe = models.BooleanField(blank=False)
    customer_has_loan = models.BooleanField(blank=False)

    # Converts Python obj into strings
    def __str__(self):
        # Returning self would get an infinite loop
        return f"{self.user} | {self.customer_phone_number} | {self.customer_rank} | { True if self.customer_has_loan else False}"

    @classmethod
    def create_profile(self, user, phone, token, mfe, has_loan):
        profile = Profile.objects.create(user = user, 
                                         customer_phone_number = phone,
                                         customer_token = token, 
                                         customer_mfe = mfe, 
                                         customer_has_loan = has_loan)

        profile.save()
        return profile

    @classmethod
    def create_customer(self, email, username, password, first_name, last_name) -> User:
        user = User.objects.create_user(email = email, 
                                        username = username, 
                                        password = password, 
                                        first_name = first_name, 
                                        last_name = last_name)

        return user

    @classmethod
    def create_employee(self, email, username, password, first_name, last_name) -> User:
        user = User.objects.create_user(email = email, 
                                        username = username, 
                                        password = password, 
                                        first_name = first_name, 
                                        last_name = last_name,
                                        is_staff = True)

        return user