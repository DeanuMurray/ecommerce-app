from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    is_vendor = forms.BooleanField(required=False, label='Register as a vendor')

    class Meta:
        model = User
        fields = ('username', 'email', 'is_vendor', 'password1', 'password2')
