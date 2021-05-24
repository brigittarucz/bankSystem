# from django.db import models
# from auth_app.models import Profile

# class Message(models.Model):
#     author = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add = True)


#     def __str__(self):
#         return self.author.User.username


#     def last_10_messages(self):
#         return Message.objects.order_by('-timestamp').all()[:10]