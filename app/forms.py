from django import forms
from django.contrib.auth.models import User
from .models import *

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['name', 'email', 'password']