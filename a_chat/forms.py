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