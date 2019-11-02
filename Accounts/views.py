from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.db import IntegrityError

from Accounts.forms import *

# Create your views here.

def home(request):
    ''' The first page user visits '''
    return render(request,'Accounts/home.html',{}) 


@login_required
def user_logout(request):
    ''' Logout the user from his session'''
    logout(request)
    return HttpResponseRedirect(reverse('home'))

class Login_Register(View):
    template = 'Accounts/Login_Register.html'

    def get(self, request, *args, **kwargs):
        ''' Process a get request '''
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        return render(request,self.template,{})

    def post(self, request, *args, **kwargs):
        ''' Process a post request '''
        try:
            next_page = request.GET['next']
        except:
            next_page = None

        if request.POST.get('lusername'):
            username = request.POST.get('lusername')
            password = request.POST.get('lpassword')
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    if next_page:
                        return HttpResponseRedirect(next_page)
                    return HttpResponseRedirect(reverse('home'))
            else:
                return render(request , self.template, {'error':'There is an error in username or password, please try again!'})
        elif request.POST.get('rusername'):
            username = request.POST.get('rusername')
            email = request.POST.get('remail')
            password = request.POST.get('rpassword')
            error = None
            if username is not None and email is not None and password is not None:
                if username =="" or username == " " or password == "" or password == " " or email =="" or email == " ":
                    error = "There is error in one of the fields"
                if error is not None:
                    return render(request , self.template, {'error': error})
                try:
                    newuser = User.objects.create_user(username, email, password)
                except IntegrityError:
                    return render(request , self.template, {'error':"Username exists"})
                newuser.set_password(password)
                newuser.save()
                student = Student.objects.create(user = newuser)
                student.save()
                
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request,user)

                if next_page:
                    return HttpResponseRedirect(next_page)
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request , self.template, {'error':'There is an error in your form, please try again!'})
        
        return render(request , self.template, {'error':'There is an error, please try again!'})

class User_profile(View):
    template_name = "Accounts/profile.html"

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username = kwargs['username'])
        student = get_object_or_404(Student, user = user)
        can_edit = False
        if request.user.is_authenticated and request.user == user:
            can_edit = True
        return render(request, self.template_name, {"user":user,"student":student,"can_edit":can_edit})

class User_update(View):
    template_name = "Accounts/profile_update.html"

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username = kwargs['username'])
        student = get_object_or_404(Student, user = user)
        if request.user.is_authenticated and request.user == user:
            return render(request, self.template_name, {})
        else:
            return HttpResponseRedirect(reverse('home'))    
        
        


    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username = kwargs['username'])
        student = get_object_or_404(Student, user = user)
        if request.user.is_authenticated and request.user == user:

            Form = request.POST
            print(Form)
            if Form['first_name']=="" or Form['last_name']=="" or Form['birthday']=="" or Form["email"]=="" or Form["phone"]=="":
                error = "There is an error in your form"
                return render(request, self.template_name, {"error":error})
            else:
                user.first_name = Form['first_name']
                user.last_name = Form['last_name']
                student.description = Form['description']
                student.birthdate = str(Form['birthday'])
                student.gender = Form['gender']
                student.phone = Form['phone']
                student.githublink = Form['github']
                student.facebooklink = Form['facebook']
                student.linkedinlink = Form['linkedin']
                student.instagramlink = Form['instagram']
                student.achname1 = Form['achname1']
                student.ach1 = Form['achievement1']
                student.achname2 = Form['achname2']
                student.ach2 = Form['achievement2']
                student.achname3 = Form['achname3']
                student.ach3 = Form['achievement3']
                student.achname4 = Form['achname4']
                student.ach4 = Form['achievement4']

                user.save()
                student.save()

                return HttpResponseRedirect(reverse('home'))

        return HttpResponseRedirect(reverse('home'))