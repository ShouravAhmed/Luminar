from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    username = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='profiles/',default='profiles/default_user.png')
    
    portfolio_website = models.CharField(max_length=200, blank=True, null=True)
    github_profile = models.CharField(max_length=200, blank=True, null=True)
    linkedin_profile = models.CharField(max_length=200, blank=True, null=True)
    facebook_profile = models.CharField(max_length=200, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Exprience(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    organization = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    joined_at = models.DateField(blank=True, null=True)
    leaved_at = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.organization

class Achivement(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    finished_at = models.DateField(blank=True, null=True)
    live_url = models.CharField(max_length=100, blank=True, null=True)
    source_url = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Interest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




 