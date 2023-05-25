from django.shortcuts import render
from django.http import HttpResponse
from . import views
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect,render
from django.contrib.auth import authenticate,login

def home(request):
    return render(request,"login/index.html")
def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        myuser=User.objects.create_user(username,email,password)
        myuser.save()
        messages.success(request, "your account have been successfully created")
        return redirect("signin")

    return render(request,"login/signup.html")
def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('myapp/')
        else:
            messages.error(request, "you have made an error")
            return redirect('signin')    
    return render(request,"login/signin.html")    
 