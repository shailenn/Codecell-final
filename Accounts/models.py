from django.db import models
from django.contrib.auth.models import User
from Forum.models import *

# Create your models here.

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    stream=models.CharField(max_length=10, default='Computer')
    description = models.CharField(max_length=100, blank = True)
    birthdate = models.CharField(max_length = 50, blank = True)
    gender = models.CharField(max_length = 50, choices = (("Male","Male"),("Female","Female")))
    phone = models.IntegerField( blank = True, null = True)
    githublink = models.CharField(max_length = 70, blank = True, default = "")
    facebooklink = models.CharField(max_length = 70, blank = True, default = "")
    instagramlink = models.CharField(max_length = 70, blank = True, default = "")
    linkedinlink = models.CharField(max_length = 70, blank = True, default = "")
    achname1 = models.CharField(max_length = 70, blank = True, default = "")
    ach1 = models.CharField(max_length = 100, blank = True, default = "")
    achname2 = models.CharField(max_length = 70, blank = True, default = "")
    ach2 = models.CharField(max_length = 100, blank = True, default = "")
    achname3 = models.CharField(max_length = 70, blank = True, default = "")
    ach3 = models.CharField(max_length = 100, blank = True, default = "")
    achname4 = models.CharField(max_length = 70, blank = True, default = "")
    ach4 = models.CharField(max_length = 100, blank = True, default = "")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name="Student"
        verbose_name_plural="Students"



# Monkey Patching
def doubts_asked(self):
    return Forum_question.objects.all().filter(user = self).count()

def doubts_solved(self):
    return Forum_answer.objects.all().filter(user = self).count()

def total_users(self):
    return User.objects.all().count()

User.add_to_class("doubts_asked",doubts_asked)
User.add_to_class("doubts_solved",doubts_solved)
User.add_to_class("total_users", total_users)