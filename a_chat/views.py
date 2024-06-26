from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse
from django.contrib import messages
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
    else:
        if request.user not in chat_group_name.members.all():
            chat_group_name.members.add(request.user)
    
    # if chat_group_name.groupchat_name:
    #     if request.user not in chat_group_name.members.all():
    #         if request.user.emailaddress_set.filter(verified=True).exists():
    #             chat_group_name.members.add(request.user)
    #         else:
    #             messages.warning(request, 'Your email needs to be verified before joining this chatroom.')
    #             return redirect('profile-settings')
            
    if chat_group_name.groupchat_name:
        if request.user not in chat_group_name.members.all():
            chat_group_name.members.add(request.user)

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

@login_required
def create_groupchat(request):
    form = NewGroupForm()

    if request.method == "POST":
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)

    context = {
        'form': form
    }
    return render(request, 'a_chat/create_groupchat.html', context)

@login_required
def chatroom_edit_view(request, chatroom_name):
    # Fetch the chat group based on the group_name
    chat_group_instance = get_object_or_404(chat_group, group_name=chatroom_name)
    
    # Check if the current user is the admin of the chat group
    if request.user != chat_group_instance.admin:
        raise Http404()
    
    # Initialize the form with the current chat group instance
    form = ChatRoomEditForm(instance=chat_group_instance)
    
    # Handle POST request
    if request.method == 'POST':
        form = ChatRoomEditForm(request.POST, instance=chat_group_instance)
        if form.is_valid():
            form.save()
            
            # Handle removal of members if any
            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                chat_group_instance.members.remove(member)  
            
            # Redirect to the chatroom after saving
            return redirect('chatroom', chatroom_name=chatroom_name)
    
    # Prepare context for rendering the template
    context = {
        'form': form,
        'chat_group': chat_group_instance
    }
    
    # Render the edit chatroom template
    return render(request, 'a_chat/edit_chatroom.html', context)
    # return render(request, 'a_chat/edit_chatroom.html')

@login_required
def chatroom_delete_view(request, chatroom_name):
    chat_group_instance = get_object_or_404(chat_group, group_name=chatroom_name)
    if request.user != chat_group_instance.admin:
        raise Http404()
    
    if request.method == "POST":
        chat_group_instance.delete()
        messages.success(request, 'Chatroom deleted')
        return redirect('home')
    
    return render(request, 'a_chat/chatroom_delete.html', {'chat_group':chat_group_instance})

@login_required
def chatroom_leave_view(request, chatroom_name):
    chat_group_instance = get_object_or_404(chat_group, group_name=chatroom_name)
    if request.user not in chat_group_instance.members.all():
        raise Http404()
    
    if request.method == "POST":
        chat_group_instance.members.remove(request.user)
        messages.success(request, 'You left the Chat')
        return redirect('home')
    
    
def chat_file_upload(request, chatroom_name):
    chat_group_instance = get_object_or_404(chat_group, group_name=chatroom_name)
    
    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = group_message.objects.create(
            file = file,
            author = request.user, 
            group = chat_group_instance,
        )
        channel_layer = get_channel_layer()
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(channel_layer.group_send)(
            chatroom_name, event
        )
    return HttpResponse()

