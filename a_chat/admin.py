from django.contrib import admin
from .models import chat_group, group_message

# Register your models here.
admin.site.register(chat_group)
admin.site.register(group_message)