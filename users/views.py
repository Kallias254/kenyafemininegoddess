from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from . models import Editpage

from django.shortcuts import render,redirect,HttpResponse
from django.http import Http404


def home(request):
    # Fetch all the sections from the database based on the section names
    hnew = Editpage.objects.filter(section_name='hnew').first()
    hneww = Editpage.objects.filter(section_name='hneww').first()
    hnewww = Editpage.objects.filter(section_name='hnewww').first()
    Programme1 = Editpage.objects.filter(section_name='Programme1').first()
    Programme2 = Editpage.objects.filter(section_name='Programme2').first()
    Programme3 = Editpage.objects.filter(section_name='Programme3').first()
    about_us = Editpage.objects.filter(section_name='about_us').first()
    mission = Editpage.objects.filter(section_name='mission').first()
    vision = Editpage.objects.filter(section_name='vision').first()
    volunteer = Editpage.objects.filter(section_name='Volunteer').first()
    footer = Editpage.objects.filter(section_name='footer').first()
    team1 = Editpage.objects.filter(section_name='team1').first()
    team2 = Editpage.objects.filter(section_name='team2').first()
    team3 = Editpage.objects.filter(section_name='team3').first()
    home_section = Editpage.objects.filter(section_name='home_section').first()

    # Add all the variables to the context dictionary
    content = {
        'Programme1': Programme1,
        'Programme2': Programme2,
        'Programme3': Programme3,
        'hnew': hnew,
        'hneww': hneww,
        'hnewww': hnewww,
        'about_us': about_us,
        'mission': mission,
        'vision': vision,
        'volunteer': volunteer,
        'footer': footer,
        'team1': team1,
        'team2': team2,
        'team3': team3,
        
    }

    return render(request, 'index.html', content)

def aboutus(request):
    aboutUs = Editpage.objects.filter(section_name='aboutUs').first()
    footer = Editpage.objects.filter(section_name='footer').first()
    volunteer = Editpage.objects.filter(section_name='Volunteer').first()
    content = {
        'volunteer': volunteer,
        'footer': footer,
        'aboutUs': aboutUs,
        
    }
    
    return render(request, 'aboutus.html', content)

def programs(request):
    footer = Editpage.objects.filter(section_name='footer').first()
    our_programs = Editpage.objects.filter(section_name='our_Programs').first()
    reach = Editpage.objects.filter(section_name='reach').first()
    volunteer = Editpage.objects.filter(section_name='Volunteer').first()

    content = {
        'our_programs': our_programs,
        'footer': footer,
        'reach': reach,
        'volunteer': volunteer,
       
    }
    return render(request, 'programs.html', content)

def ourteam(request):
    volunteer = Editpage.objects.filter(section_name='Volunteer').first()
    footer = Editpage.objects.filter(section_name='footer').first()
    team1 = Editpage.objects.filter(section_name='team1').first()
    team2 = Editpage.objects.filter(section_name='team2').first()
    team3 = Editpage.objects.filter(section_name='team3').first()
    content = {
       
        'volunteer': volunteer,
        'footer': footer,
        'team1': team1,
        'team2': team2,
        'team3': team3,
     
    }
    
    return render(request, 'ourteam.html', content)

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