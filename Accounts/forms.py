from django import forms
from Accounts.models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model=User
        fields=('username','password','email')

# class StudentForm(forms.ModelForm):
#     class Meta:
#         model=Student
#         fields=('year','div','branch','rollno')