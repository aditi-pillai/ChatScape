from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import *
from .forms import *

# Create your views here.
@login_required
def chat_view(request, chatroom_name="group-chat1"):
    chat_group_name = get_object_or_404(chat_group, group_name=chatroom_name)
    chat_messages = chat_group_name.chat_messages.all()[:30]
    form = ChatMessageCreationForm()
    
    other_user = None
    if chat_group_name.is_private:
        if request.user not in chat_group_name.members.all():
            raise Http404()
        for member in chat_group_name.members.all():
            if member!=request.user:
                other_user = member
                break

    if request.htmx:
        form = ChatMessageCreationForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group_name
            message.save()
            context = {
                'message': message,
                'user' : request.user   
            }

            return render(request, 'a_chat/partials/chat_message_p.html', context)
    
    context = {
        'chat_messages': chat_messages,
        'chat_group': chat_group_name,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name
    }

    return render(request, 'a_chat/chat_end.html', context)

@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')

    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = chat_group.objects.create(is_private=True)
                chatroom.members.add(other_user, request.user)
    
    else:
        chatroom = chat_group.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)
    
    return redirect('chatroom', chatroom.group_name)
