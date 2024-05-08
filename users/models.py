from django.db import models
from django.contrib.auth.models import AbstractUser
from .manage import *

# Create your models here.


class UserProfile(AbstractUser):
    username =models.CharField(max_length=255, unique=True, primary_key=True)
    email =models.EmailField(unique=True)
    profile_picture =models.ImageField(upload_to='profile_pictures/')
    address_line1 =models.CharField(max_length=100)
    city =models.CharField(max_length=100)
    state =models.CharField(max_length=100)
    pincode =models.CharField(max_length=10)
    title =models.CharField(max_length=10)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

class Blog(models.Model):
    
    CATEGORIES = (
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid19', 'Covid19'),
        ('Immunization', 'Immunization'),
    )
    
    userprofile =models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='blogs')
    title =models.CharField(max_length=100)
    image =models.ImageField(upload_to='blog_images')
    category =models.CharField(choices=CATEGORIES, max_length=50)
    summary =models.TextField()
    content =models.TextField() 
    save_as_draft =models.BooleanField()
