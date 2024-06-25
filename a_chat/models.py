from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class chat_group(models.Model):
    group_name = models.CharField(max_length=128, unique=True)
    users_online = models.ManyToManyField(User, related_name="online_in_groups", blank=True)
    def __str__(self):
        return self.group_name
    
class group_message(models.Model):
    group = models.ForeignKey(chat_group, related_name="chat_messages", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} : {self.content}"
    
    class Meta:
        ordering = ['-timestamp']
    

