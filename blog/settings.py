# KFGAPP/blog/settings.py

from pathlib import Path
import os
import dj_database_url
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Read from environment variables, with local defaults if necessary
SECRET_KEY = config('SECRET_KEY', default='local_dev_insecure_secret_key_for_KFGAPP_project_xyz123') # Use a strong default if needed for local
DEBUG = config('DEBUG', default=True, cast=bool) # Default to True for local dev if .env is missing DEBUG

ALLOWED_HOSTS_STRING = config('ALLOWED_HOSTS', default='localhost,127.0.0.1')
ALLOWED_HOSTS = [s.strip() for s in ALLOWED_HOSTS_STRING.split(',')]

CSRF_TRUSTED_ORIGINS = []
# Automatically add Fly.dev host if FLY_APP_NAME is set (Fly.io sets this env var)
FLY_APP_NAME = config('FLY_APP_NAME', default=None)
if FLY_APP_NAME:
    fly_app_url = f"https://{FLY_APP_NAME}.fly.dev"
    CSRF_TRUSTED_ORIGINS.append(fly_app_url)
    if f"{FLY_APP_NAME}.fly.dev" not in ALLOWED_HOSTS: # Check specific hostname
        ALLOWED_HOSTS.append(f"{FLY_APP_NAME}.fly.dev")
# Also good to add the base Vercel domain if you ever deploy there for previews with custom domain
# VERCEL_URL = config('VERCEL_URL', default=None) # Vercel sets this env var automatically
# if VERCEL_URL and VERCEL_URL not in ALLOWED_HOSTS:
#    ALLOWED_HOSTS.append(VERCEL_URL)
#    CSRF_TRUSTED_ORIGINS.append(f"https://{VERCEL_URL}")


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = [
    'jet',
    'users.apps.UsersConfig',
    'blogapp',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'taggit',
    'import_export',
    'ckeditor_uploader',
    # 'graphene_django', # Kept commented out
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # For serving static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'users', 'templates'),
        ],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'blog.wsgi.application'

# Database Configuration
DEFAULT_SQLITE_URL = f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
DATABASE_URL_FROM_ENV = config('DATABASE_URL', default=DEFAULT_SQLITE_URL) # Fallback to SQLite if DATABASE_URL not set

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL_FROM_ENV, conn_max_age=600)
}

# Adjust PostgreSQL options if using PostgreSQL
if DATABASES['default'].get('ENGINE') == 'django.db.backends.postgresql':
    if 'OPTIONS' not in DATABASES['default'] or DATABASES['default']['OPTIONS'] is None:
        DATABASES['default']['OPTIONS'] = {}
    # For Supabase and other cloud PostgreSQL, 'require' is usually better than 'prefer'
    # but 'prefer' is safer if local PostgreSQL doesn't have SSL.
    # Since DATABASE_URL for Supabase includes sslmode, this might be redundant or can be 'require'.
    if 'sslmode' not in DATABASES['default']['OPTIONS']:
         DATABASES['default']['OPTIONS']['sslmode'] = config('DB_SSLMODE', default='prefer')


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True # Django 3.2 still uses this.
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Where collectstatic puts files
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # Where Django dev server finds your app's static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Where user uploads go

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'