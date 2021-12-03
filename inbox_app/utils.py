
from .models import text_message
from django.db.models import Q
from user_app.models import Profile


def get_text_messages(request, pk):
    receiver = Profile.objects.get(id=pk)
    messages = text_message.objects.distinct().order_by('created_at').filter(
        Q(sender=request.user.profile, receiver=receiver) |
        Q(sender=receiver, receiver=request.user.profile)
    )
    for msg in messages:
        if msg.sender != request.user.profile:
            msg.is_read = True
            msg.save()
    return messages, receiver

def inbox_preview(request):
    messages = text_message.objects.distinct().order_by('is_read', '-created_at').filter(
        Q(sender=request.user.profile) |
        Q(receiver=request.user.profile)
    )
    msg_list = list()
    taken = dict()
    for msg in messages:
        if msg.receiver == request.user.profile and msg.sender.username not in taken:
            taken[msg.sender.username] = 1
            msg_list.append(msg)
        elif msg.receiver != request.user.profile and msg.receiver.username not in taken:
            taken[msg.receiver.username] = 1
            msg_list.append(msg)
    new_msg = 0
    for msg in msg_list:
        if not msg.is_read and msg.sender != request.user.profile:
            new_msg += 1

    return msg_list, new_msg


def new_message(request):
    messages = text_message.objects.distinct().order_by('is_read', '-created_at').filter(
        Q(sender=request.user.profile) |
        Q(receiver=request.user.profile)
    )
    msg_list = list()
    taken = dict()
    for msg in messages:
        if msg.receiver == request.user.profile and msg.sender.username not in taken:
            taken[msg.sender.username] = 1
            msg_list.append(msg)
        elif msg.receiver != request.user.profile and msg.receiver.username not in taken:
            taken[msg.receiver.username] = 1
            msg_list.append(msg)
    new_msg = 0
    for msg in msg_list:
        if not msg.is_read and msg.sender != request.user.profile:
            new_msg += 1

    return new_msg

def new_notification(request):
    profile = request.user.profile
    notifi = profile.notification_set.filter(is_read=False)
    return len(notifi)

def notification_list(request):
    profile = request.user.profile
    return profile.notification_set.all()
    
def read_notification(request):
    profile = request.user.profile
    notifi = profile.notification_set.filter(is_read=False)
    for n in notifi:
        n.is_read = True
        n.save()

