from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class CreateThread(forms.ModelForm):
    class Meta:
        model = models.Thread
        fields = ['title','text']


# user sign up form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )


class EditProfileForm(UserChangeForm):

    class Meta:
        model = models.Profile
        fields = (
            'email',
            'first_name',
            'last_name',
            'gender',
            'phone',
            'image',
            'password'

        )