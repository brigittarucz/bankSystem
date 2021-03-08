from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from auth_app.models import Profile

def main(request):
    context = {
        'users': Profile.objects.all()
    }

    print(context)

    return render(request, 'employee_app/main.html', context)
