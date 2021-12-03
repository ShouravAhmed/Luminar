from django.contrib import admin
from .models import text_message, Notification


admin.site.register(text_message)
admin.site.register(Notification)

