from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserDetail
class UserRegisterForm(UserCreationForm):
     mobile=forms.CharField()
     class Meta:
        model=User
        fields=['first_name','last_name','mobile','email','username','password1','password2']

class UserUpdate(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username']

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model=UserDetail
        fields=['mobile','image']
