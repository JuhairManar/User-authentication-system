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
        model = UserProfile
        fields = [ 'first_name', 'last_name', 'email', 'profile_picture','username','password1', 'password2',  'address_line1', 'city', 'state', 'pincode']
        # fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'profile_picture', 'address_line1', 'city', 'state', 'pincode']
        # fields='__all__'


# for field in User._meta.get_fields():
#     print(field.name)


class Create_Blog(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
        self.fields['save_as_draft'].required = False

    class Meta:
        model = Blog
        fields = ['title', 'image', 'category', 'summary', 'content', 'save_as_draft']

class ChangeUserData(UserChangeForm):
    password=None #it won't show password field
    class Meta:
        model=UserProfile
        fields=['first_name', 'last_name', 'email', 'profile_picture','username',  'address_line1', 'city', 'state', 'pincode']
