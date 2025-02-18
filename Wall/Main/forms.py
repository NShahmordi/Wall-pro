from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from .models import Users, Advertisement, Message, AdvertisementImage
from .widgets import *

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Users
        fields = ("username","first_name","last_name","email","phone_number")
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "phone_number":"Phone Number"
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.NumberInput(attrs= {"class":"form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Users
        fields = ("username", "first_name", "last_name", "email", "phone_number")

class SignUpForm(CustomUserCreationForm):
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password (again)",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    class Meta:
        model = Users
        fields = ("username", "first_name", "last_name", "email",)
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "phone_number":"Phone Number"
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.NumberInput(attrs= {"class":"form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'price', 'publication_date', 'category', 'city']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
class AdvertismentImageForm(forms.ModelForm):
    class Meta:
        model = AdvertisementImage
        fields = ('image',)
        widgets = {
            'image': MultipleFileInput(attrs={'multiple': True, 'accept': 'image/*'}),
        }

    def save(self, advertisement, *args, **kwargs):
        images = self.files.getlist('image')
        for image in images:
            AdvertisementImage.objects.create(advertisement=advertisement, image=image)
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
