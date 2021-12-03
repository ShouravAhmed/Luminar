from django.shortcuts import render, redirect
from django.contrib import messages

from .utils import get_text_messages, inbox_preview, new_message, new_notification, notification_list, read_notification
from .models import text_message

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def chatbox(request, pk):
    if str(request.user.profile.id) == str(pk):
        messages.error(request, "You can't chat with yourself")
        return redirect('dashboard')

    text_messages, receiver = get_text_messages(request, pk)
    
    if request.method == 'POST':
        message = request.POST['message']
        msg = text_message.objects.create(
            body = message,
            sender = request.user.profile,
            receiver = receiver
        )
        msg.save()
        redirect('chatbox', pk)

    context = {
        'text_messages':text_messages, 
        'receiver':receiver,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }    
    
    return render(request, 'inbox_app/chatbox.html', context)

@login_required(login_url='login')
def inbox(request):
    msg_list, new_msg = inbox_preview(request)
    context = {
        'msg_list':msg_list,
        'new_msg':new_msg,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'inbox_app/inbox.html', context)

@login_required(login_url='login')
def notification(request):
    notifi_list = notification_list(request)
    context = {
        'notifi_list':notifi_list,
        'new_msg':new_message(request),
        'new_notifi':new_notification(request),
    }
    return render(request, 'inbox_app/notification.html', context)

@login_required(login_url='login')
def mark_all_read(request):
    read_notification(request)
    return redirect('notification')