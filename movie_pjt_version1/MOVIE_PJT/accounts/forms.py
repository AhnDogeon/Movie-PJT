from django import forms
from .models import User
# from django.contrib.auth import get_user_model 은 옆이랑 같은 말이다

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

class UserCustomCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserCustomAuthenticationForm(AuthenticationForm):

    class Meta(AuthenticationForm):
        model = User