from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserCreationForm(UserCreationForm):
    username = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['username']
