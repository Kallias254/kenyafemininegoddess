# KFGAPP/blog/settings.py

from pathlib import Path
import os

# It's good practice to keep these imports if you plan to use environment variables
# for sensitive data in the future (especially for production), but for now,
# we are hardcoding the SQLite database.
# import dj_database_url # Not strictly needed for the hardcoded SQLite config below
# from decouple import config # Not strictly needed for the hardcoded SQLite config below

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# REPLACE THIS WITH YOUR ACTUAL SECRET KEY FROM YOUR ORIGINAL FILE
SECRET_KEY = 'jqx3e+sq2(sja+kuxr6(t5oijbe6(9jaf!1ieat0raf0nb&w=w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # Keep True for local development

ALLOWED_HOSTS = ['*'] # Allows all hosts for local development, restrict for production

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Application definition
INSTALLED_APPS = [
    'jet', # Admin theme, ensure it's compatible or consider removing if causing issues
    # 'graphene_django', # For GraphQL, if you're not using it, you can comment it out.
                       # If you are, ensure 'graphql_core>=2.1' or similar is installed.
    'users.apps.UsersConfig', # Assuming this is your users app configuration
    'blogapp',                # Your main app, or 'blogapp.apps.BlogappConfig' if it exists
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',               # WYSIWYG editor
    'taggit',                 # For tagging functionality
    'import_export',          # For admin import/export
    'ckeditor_uploader',      # For uploading images within CKEditor. Requires configuration.
                              # Ensure MEDIA_ROOT and MEDIA_URL are set correctly for this.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # For serving static files, good for production, fine for dev
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls' # Points to KFGAPP/blog/urls.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django will look for templates in these directories first
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),      # Project-level templates (KFGAPP/templates/)
            os.path.join(BASE_DIR, 'users', 'templates'), # Templates inside users app (KFGAPP/users/templates/)
                                                      # This makes templates like 'index.html' in users/templates directly findable.
                                                      # If you prefer app-namespacing (e.g. 'users/index.html'),
                                                      # you'd put templates in users/templates/users/index.html
                                                      # and APP_DIRS=True would handle it.
                                                      # For now, this matches your observed structure.
        ],
        'APP_DIRS': True, # Django will also look inside each app's 'templates' directory (e.g., blogapp/templates/)
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application' # For WSGI deployment

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Commented out PostgreSQL configuration
# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'neondb',
#     'USER': 'neondb_owner',
#     'PASSWORD': '4MUPmrWS7xwV',
#     'HOST': 'ep-cool-dew-a4fl1wt4.us-east-1.aws.neon.tech',
#     'PORT': '5432',
#     'OPTIONS': {'sslmode': 'require'},
#   }
# }

# SQLite configuration for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', # This will create db.sqlite3 in your KFGAPP project root
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC' # Or your local timezone, e.g., 'Africa/Nairobi'
USE_I18N = True
USE_L10N = True # Deprecated in Django 4.0, but you are on 3.2.
USE_TZ = True   # Recommended to keep True for timezone-aware datetimes


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/' # URL prefix for static files

# Directory where `collectstatic` will gather all static files for deployment.
# This should be different from any directory in STATICFILES_DIRS.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional locations of static files for Django's development server to find.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # KFGAPP/static/
]

# For WhiteNoise, to serve static files efficiently in production (and dev if used)
# WHITENOISE_MANIFEST_STRICT = False # You had this, usually not needed unless specific issues arise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files (user-uploaded files like images for Events)
MEDIA_URL = '/media/' # URL prefix for media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Absolute filesystem path to the directory for user-uploaded files
                                            # Create this 'media' directory in KFGAPP project root: mkdir media

# UPLOADCARE settings (if you are using Uploadcare for image/file uploads)
# UPLOADCARE = {
#   'pub_key': 'f914008525312051b54c',  # Replace with your actual Uploadcare public key
#   'secret': '06f605e3fa31437f2a51',   # Replace with your actual Uploadcare secret key
# }
# Note: If using Uploadcare extensively, you might not need MEDIA_ROOT/MEDIA_URL for those specific fields,
# as Uploadcare hosts the files. However, standard Django ImageFields/FileFields will use MEDIA_ROOT.

# CKEditor settings
CKEDITOR_UPLOAD_PATH = "uploads/" # Subdirectory within MEDIA_ROOT for CKEditor uploads.
                                  # So files will go to KFGAPP/media/uploads/
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full', # Or 'basic', or a custom toolbar configuration
        'height': 300,
        'width': '100%',
    },
}

# Django Jet admin theme settings (optional, defaults are usually fine)
# JET_SIDE_MENU_COMPACT = True
# JET_THEME = 'light-blue'

# Ensure your custom user model is specified if you have one in the 'users' app
# Example: AUTH_USER_MODEL = 'users.CustomUser'
# If you're using Django's default User model, you don't need AUTH_USER_MODEL.
# Your UsersConfig in INSTALLED_APPS suggests you might have custom user setup.
# If users/models.py defines a custom user, ensure AUTH_USER_MODEL is set.
# If not, and users app is just for profiles or views, it's fine.