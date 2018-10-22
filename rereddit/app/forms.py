from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker', 'readonly':'true'})


class CreateThread(forms.Form):


    title = forms.CharField(max_length=140)

    text = forms.CharField(max_length=2000,
                           widget=forms.Textarea())



class UserCreateForm(UserCreationForm):
    # username = forms.CharField(label="username", required=True)
    # password1 = forms.CharField(label="password1", required=True)
    # password2 = forms.CharField(label="password2", required=True)
    # email = forms.EmailField(label="email", required=True)
    # first_name = forms.CharField(label="first_name", required=True)
    # last_name = forms.CharField(label="last_name", required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name", "last_name")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name',"email")



class EditProfileForm(forms.ModelForm):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'), ('Unisex', 'Unisex/Parody'))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Gender')
    birthday = forms.DateField( input_formats=['%d-%m-%Y'],label=('Birthday'), widget=forms.DateInput(format= "%d-%m-%Y",attrs={'class': 'datepicker'}))
    class Meta:
        model = models.Profile
        # widgets = {
        #     'birthday': forms.DateInput(attrs={'class': 'datepicker'}),
        # }
        fields = (
            'gender',
            'birthday',
            'phone',
            'image'
        )

