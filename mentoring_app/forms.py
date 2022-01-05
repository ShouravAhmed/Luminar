from django.forms import ModelForm
from django import forms

from .models import MentoringProgram, Feature, UserResponse


class MentoringProgramForm(ModelForm):
    class Meta:
        model = MentoringProgram
        fields = ['title', 'description', 'cover_picture']
    
    # def __init__(self, *args, **kwargs):
    #     super(ProfileForm, self).__init__(*args, **kwargs)

    #     for name,field in self.fields.items():
    #         field.widget.attrs.update({
    #             'class':'input',
    #         })

class FeatureForm(ModelForm):    
    class Meta:
        model = Feature
        fields = ['title', 'description', 'is_personal_interest']


class UserResponseForm(ModelForm):
    class Meta:
        model = UserResponse
        fields = ['exp_level', 'description']


