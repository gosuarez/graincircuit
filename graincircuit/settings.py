from pathlib import Path
import os
from django.contrib.messages import constants as message_constants

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
if 'testserver' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('testserver')

SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')

# Application Definition
INSTALLED_APPS = [
    'bookmarks',
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'graincircuit.urls'
WSGI_APPLICATION = 'graincircuit.wsgi.application'

# Template Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

# Authentication
AUTH_USER_MODEL = 'bookmarks.User'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and Media Files
USE_AZURE_STORAGE = os.getenv('USE_AZURE_STORAGE', 'False') == 'True'
if USE_AZURE_STORAGE:
    AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
    AZURE_MEDIA_CONTAINER = os.getenv('AZURE_MEDIA_CONTAINER')
    AZURE_STATIC_CONTAINER = os.getenv('AZURE_STATIC_CONTAINER')

    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.azure_storage.AzureStorage',
            'OPTIONS': {
                'account_name': AZURE_ACCOUNT_NAME,
                'account_key': AZURE_ACCOUNT_KEY,
                'azure_container': AZURE_MEDIA_CONTAINER,
                'custom_domain': f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net",
            },
        },
        'staticfiles': {
            'BACKEND': 'storages.backends.azure_storage.AzureStorage',
            'OPTIONS': {
                'account_name': AZURE_ACCOUNT_NAME,
                'account_key': AZURE_ACCOUNT_KEY,
                'azure_container': AZURE_STATIC_CONTAINER,
                'custom_domain': f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net",
            },
        },
    }

    STATIC_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{
        AZURE_STATIC_CONTAINER}/"
    MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{
        AZURE_MEDIA_CONTAINER}/"
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Messages Framework
MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}
