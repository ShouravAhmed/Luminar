from django.contrib import admin

from .models import MentoringProgram, Feature, UserResponse, UserEnroll, MmTask, MmChat

admin.site.register(MentoringProgram)
admin.site.register(Feature)
admin.site.register(UserResponse)
admin.site.register(UserEnroll)
admin.site.register(MmTask)
admin.site.register(MmChat)
