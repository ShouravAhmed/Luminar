from django.db import models
import uuid
from user_app.models import Profile

class text_message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reciver')
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.sender.username + "->" + self.receiver.username

class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    redirect_url = models.CharField(max_length=100, blank=True, null=True)

    reciver = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


    