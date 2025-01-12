from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
from django import forms
from .models import CustomUser

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']  # Add other fields you want the user to be able to update
