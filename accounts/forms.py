from typing import Any
from django.forms import EmailField, CharField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms

class UserCreationForm(UserCreationForm):
    email = EmailField(
        label=_("Email address"), 
        required=True,
        help_text=_("Required."),
        widget=forms.EmailInput(
            attrs={'class':'form-control',
                   'placeholder':'email@example.com',}
        )
        )
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        placeholders = {
            'username': 'Enter username',
            'password1': 'Enter password',
            'password2': 'Re-enter password',
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({
                'class':'form-control',
                'placeholder':placeholder,
            })

class AuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter username'}
            )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter password'}
            )