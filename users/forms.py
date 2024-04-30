from django.contrib.auth.models import User #importing user for user form
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
#UserCreationForm #importing user form
#UserChangeForm  for user data change
from django import forms #this is for showing required filed message
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .models import *

# User._meta.get_fields()

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'required'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'id': 'required'}))
    profile_picture = forms.ImageField(required=True) 
    address_line1 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'required'}))
    city = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'required'}))
    state = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'required'}))
    pincode = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'id': 'required'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profile_picture', 'address_line1', 'city', 'state', 'pincode']


# for field in User._meta.get_fields():
#     print(field.name)

class ChangeUserData(UserChangeForm):
    password=None #it won't show password field
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
