from django.db import models
import uuid
from user_app.models import Profile


class MentoringProgram(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='admin', blank=True, null=True)
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    cover_picture = models.ImageField(blank=True, null=True, upload_to='',default='default_cover.jpg')

    trainer = models.ManyToManyField(Profile, related_name='trainer', blank=True)
    moderator = models.ManyToManyField(Profile, related_name='moderator', blank=True)

    is_published = models.BooleanField(default=False)
    is_enroll_on = models.BooleanField(default=False)
    is_program_started = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Feature(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    feature_program = models.ForeignKey(MentoringProgram, on_delete=models.CASCADE, related_name='feature_program', blank=True, null=True)
    
    title = models.CharField(max_length=100)
    description = models.TextField()

    is_personal_interest = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class UserResponse(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='feature', blank=True, null=True)
    
    userresponse_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='userresponse_profile', blank=True, null=True)

    exp_level = models.PositiveIntegerField(default=0)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.feature.title) + str(self.exp_level)
    

class UserEnroll(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    userenroll_program = models.ForeignKey(MentoringProgram, on_delete=models.CASCADE, related_name='userenroll_program', blank=True, null=True)
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_profile', blank=True, null=True)
    
    mentor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='mentor', blank=True, null=True)
    mentee = models.ManyToManyField(Profile, related_name='mentee', blank=True)

    is_submited = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user_profile.username


class MmTask(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    mmtask_program = models.ForeignKey(MentoringProgram, on_delete=models.CASCADE, related_name='mmtask_program', blank=True, null=True)
    
    mmtask_mentor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='mmtask_mentor', blank=True, null=True)
    mmtask_mentee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='mmtask_mentee', blank=True, null=True)

    title = models.CharField(max_length=100)
    description = models.TextField()

    deadline = models.DateField()

    is_done = models.BooleanField(default=False)
    is_evaluated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_profile.username


class MmChat(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    mmchat_program = models.ForeignKey(MentoringProgram, on_delete=models.CASCADE, related_name='mmchat_program', blank=True, null=True)
    
    mmchat_mentor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='mmchat_mentor', blank=True, null=True)
    mmchat_mentee = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='mmchat_mentee', blank=True, null=True)

    mmchat_sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='mmchat_sender', blank=True, null=True)
    mmchat_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='mmchat_receiver', blank=True, null=True)
    
    body = models.TextField()

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username + "->" + self.receiver.username




