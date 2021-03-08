from django.contrib import admin
from .models import Profile

# Customizing model fields shown in the default Admin Panel
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user', 'customer_phone_number']

admin.site.register(Profile, ProfileAdmin)  

# TO DISCUSS:
# Users should only be registered through /auth/register
# Need of transaction & accounts to be linked with user profile
# Payments? Where have you used models.py __str__ transaction_app & what for?
# Error logging available from django