from django.db import models
from django.contrib.auth.models import User
import shortuuid
from PIL import Image
import os

# Create your models here.
class chat_group(models.Model):
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    groupchat_name = models.CharField(max_length=128, null=True, blank=True)
    admin = models.ForeignKey(User, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
    users_online = models.ManyToManyField(User, related_name="online_in_groups", blank=True)
    members = models.ManyToManyField(User, related_name="chat_groups", blank=True)
    is_private = models.BooleanField(default=False)
    def __str__(self):
        return self.group_name
    
class group_message(models.Model):
    group = models.ForeignKey(chat_group, related_name="chat_messages", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to="files/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.name)
        else:
            return None

    def __str__(self):
        if self.content:
            return f'{self.author.username} : {self.content}'
        elif self.file:
            return f'{self.author.username} : {self.filename}'
    
    class Meta:
        ordering = ['-timestamp']
    
    @property    
    def is_image(self):
        try:
            image = Image.open(self.file) 
            image.verify()
            return True 
        except:
            return False
    
    

