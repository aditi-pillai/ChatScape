from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.
@login_required
def chat_view(request):
    chat_group_name = get_object_or_404(chat_group, group_name="group-chat1")
    chat_messages = chat_group_name.chat_messages.all()[:30]
    form = ChatMessageCreationForm()
    # if request.htmx:
    #     form = ChatMessageCreationForm(request.POST)
    #     if form.is_valid:
    #         message = form.save(commit=False)
    #         message.author = request.user
    #         message.group = chat_group_name
    #         message.save()
    #         # chat_messages = chat_group_name.chat_messages.all()
    #         context = {
    #             'message': message,
    #             'user' : request.user
    #         }
    #         # return redirect('home')
    #         return render(request, 'a_chat/chat_end.html', context)
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
    # chat_messages = chat_group_name.chat_messages.all()    
    return render(request, 'a_chat/chat_end.html', {'chat_group': chat_group_name, 'chat_messages': chat_messages, 'form': form})

# @login_required
# def chat_view(request):
#     chat_group_name = get_object_or_404(chat_group, group_name="group-chat1")
#     chat_messages = chat_group_name.chat_messages.all()[:30]
#     form = ChatMessageCreationForm()

#     if request.method == "POST":
#         form = ChatMessageCreationForm(request.POST)
#         if form.is_valid():  # Corrected method call with parentheses
#             message = form.save(commit=False)
#             message.author = request.user
#             message.save()  # Save the message to the database
#             if request.htmx:
#                 # Handle your HTMX response here
#                 pass
#             else:
#                 # Handle non-HTMX POST request response here
#                 pass
#     else:
#         # Handle GET request here
#         pass

#     # Your context and render or HTTP response goes here