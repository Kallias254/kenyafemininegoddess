from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from taggit.managers import TaggableManager
from html import unescape
from django.utils.html import strip_tags
from shortuuid.django_fields import ShortUUIDField
from pyuploadcare.dj.models import ImageField
from ckeditor.fields import RichTextField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(default='Edit your Bio!')
    website = models.CharField(max_length=40)

    def __str__(self):
        return self.user.get_username()
    
class Editpage(models.Model):
    SECTION_CHOICES = [
        ('about_us', 'About Us'),
        ('mission', 'Our Mission'),
        ('vision', 'Vision'),
    ]

    section_name = models.CharField(max_length=100, choices=SECTION_CHOICES, unique=True)
    content = RichTextField()

    def __str__(self):
        return self.get_section_name_display()
    
    
