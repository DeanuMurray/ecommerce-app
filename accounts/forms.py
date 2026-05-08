from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    """Registration form that supports vendor/buyer role selection.

    Adds an email field with uniqueness validation and an is_vendor
    checkbox so users can register as vendors or buyers.
    """

    email = forms.EmailField(required=True, label='Email address')
    is_vendor = forms.BooleanField(required=False, label='Register as a vendor')

    class Meta:
        model = User
        fields = ('username', 'email', 'is_vendor', 'password1', 'password2')

    def clean_email(self):
        """Ensure the email address is not already registered."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'An account with this email address already exists.'
            )
        return email
