from django.shortcuts import render

from django.shortcuts import render

from accounts_app_account.models import Account 
from auth_app.models import Profile

def index(request):
    return render(request, 'chat/index.html')

#docker run -p 6379:6379 -d redis:5 run this container to get up and running the chat
def room(request, room_name):
    user = request.user
    print(user)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'user': user
    })





def accounts_view(request):
    user = request.user
    # path = request.path
    # print(path)
    profile = Profile.objects.get(user=user)
    user_account = Account.objects.filter(account_user_fk=profile)
    context = {
        "user": user,
        "user_accounts": user_account,
    }
    return render(request, "accounts_app_account/account.html", context)

