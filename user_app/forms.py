from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import ModelForm
from user_app import models
from django import forms

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name':'Name', 
            'username':'Username',
            'email':'Email Address',
            'password1':'Password', 
            'password2':'Password confirmation'
        }
    
    # def __init__(self, *args, **kwargs):
    #     super(UserRegistrationForm, self).__init__(*args, **kwargs)

    #     for name,field in self.fields.items():
    #         field.widget.attrs.update({
    #             'class':'input',
    #         })
            
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already Registered")
        elif email == "":
            raise forms.ValidationError("Email Address is Required")
        
        return email


class ProfileForm(ModelForm):
    
    class Meta:
        model = models.Profile
        fields = ['name', 'intro', 'location', 'profile_picture', 'bio', 'linkedin_profile', 'github_profile', 'facebook_profile', 'portfolio_website']
    
    # def __init__(self, *args, **kwargs):
    #     super(ProfileForm, self).__init__(*args, **kwargs)

    #     for name,field in self.fields.items():
    #         field.widget.attrs.update({
    #             'class':'input',
    #         })

class SkillForm(ModelForm):
    
    class Meta:
        model = models.Skill
        fields = ['title', 'description']
    
    # def __init__(self, *args, **kwargs):
    #     super(ModelForm, self).__init__(*args, **kwargs)

    #     for name,field in self.fields.items():
    #         field.widget.attrs.update({
    #             'class':'input',
    #         })

class ExprienceForm(ModelForm):
    
    class Meta:
        model = models.Exprience
        fields = ['role', 'organization', 'description', 'joined_at', 'leaved_at']
    
    # def __init__(self, *args, **kwargs):
    #     super(ModelForm, self).__init__(*args, **kwargs)

    #     for name,field in self.fields.items():
    #         field.widget.attrs.update({
    #             'class':'input',
    #         })

class AchivementForm(ModelForm):
    
    class Meta:
        model = models.Achivement
        fields = ['title', 'description']
    
    # def __init__(self, *args, **kwargs):
    #     super(ModelForm, self).__init__(*args, **kwargs)

    #     for name,field in self.fields.items():
    #         field.widget.attrs.update({
    #             'class':'input',
    #         })

class ProjectForm(ModelForm):
    
    class Meta:
        model = models.Project
        fields = ['title', 'description', 'live_url', 'source_url', 'finished_at']
    
    # def __init__(self, *args, **kwargs):
    #     super(ModelForm, self).__init__(*args, **kwargs)

    #     for name,field in self.fields.items():
    #         field.widget.attrs.update({
    #             'class':'input',
    #         })

class InterestForm(ModelForm):
    
    class Meta:
        model = models.Interest
        fields = ['title', 'description']
    
    # def __init__(self, *args, **kwargs):
    #     super(ModelForm, self).__init__(*args, **kwargs)

    #     for name,field in self.fields.items():
    #         field.widget.attrs.update({
    #             'class':'input',
    #         })

