from django import forms
from django.contrib.auth.models import User


from .models import Notification
from .models import Profile
from .models import SocialLink


# Profile form
class ProfileForm(forms.ModelForm):
    """docstring for ProfileForm"""

    class Meta:
        model = Profile
        fields = "__all__"


# Registration Form
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"type": "email"}),
        }


# update personal info form
class UpdatePersonalInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class UpdateBioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]


# update profile picture
class UpdateProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_pic",
        ]


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )
