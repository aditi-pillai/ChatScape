from django.forms import ModelForm
from django import forms
from .models import *

class ChatMessageCreationForm(ModelForm):
    class Meta:
        model = group_message
        fields = ['content']
        widgets = {
            # 'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter message here...'})
            'content': forms.TextInput(attrs={'class': 'p-4 text-black', 'placeholder': 'Type a message...', 'max_length': '1000', 'autofocus':True, 'autocomplete': 'off'})
        }

class NewGroupForm(ModelForm):
    class Meta:
        model = chat_group
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Enter group name here...',
                'class': 'p-4 text-black',
                'maxlength': '300',
                'autofocus': True,
            })
        }

class ChatRoomEditForm(ModelForm):
    class Meta:
        model = chat_group
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name' : forms.TextInput(attrs={
                'class': 'p-4 text-xl font-bold mb-4', 
                'maxlength' : '300', 
                }),
        }