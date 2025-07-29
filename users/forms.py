from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "w-full px-4 py-2 border rounded-md"}),
            "email": forms.EmailInput(attrs={"class": "w-full px-4 py-2 border rounded-md"}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image", "contact_number"]
        widgets = {
            "contact_number": forms.TextInput(attrs={"class": "w-full px-4 py-2 border rounded-md"}),
        }