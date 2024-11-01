from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from . models import Editpage

from django.shortcuts import render,redirect,HttpResponse
from django.http import Http404


def home(request):
    about_us = Editpage.objects.filter(section_name='about_us').first()
    mission = Editpage.objects.filter(section_name='mission').first()
    vision = Editpage.objects.filter(section_name='vision').first()

    content = {
        'about_us': about_us,
        'mission': mission,
        'vision': vision,
    }
    print("Static Content for About Us:", Editpage.objects.filter(section_name='About Us').all())
    return render(request, 'index.html', content)

def aboutus(request):
    
    return render(request, 'aboutus.html')

def programs(request):
    
    return render(request, 'programs.html')

def ourteam(request):
    
    return render(request, 'ourteam.html')

def contactus(request):
    
    return render(request, 'contactus.html')

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken!')
                return redirect('.')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered!')
                return redirect('.')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                user = auth.authenticate(username=username, password=password1)
                auth.login(request, user)
                return redirect('blog')
        else:
            messages.info(request, 'Password not matching!')
            return render('.')
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('blog')
        else:
            messages.info(request, 'Invalid Credentials!')
            return redirect('.')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'logout.html')