from django import forms
from . import models



class CreateThread(forms.ModelForm):
    class Meta:
        model = models.Thread
        fields = ['title','text']
