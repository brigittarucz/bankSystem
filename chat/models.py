from django.db import models
from auth_app.models import User
from django.utils import timezone

class Message(models.Model):
    message_id = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.author.username


    #preload last 10 messages
    
    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[:10]