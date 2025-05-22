# KFGAPP/users/urls.py
from django.urls import path
from . import views # Your custom views for home, aboutus, etc.
from django.contrib.auth import views as auth_views # Django's auth views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('programs/', views.programs, name='programs'),
    path('ourteam/', views.ourteam, name='ourteam'),
    path('contactus/', views.contactus, name='contactus'),

    # Add URL patterns for login and logout if not already present
    # You might already have login if your login button works.
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'), # Example for login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Using Django's default logout
    path('register/', views.register, name='register'), # ADD THIS (points to users.views.register)
]