"""
Django settings for usanii_mtaani project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

from django.contrib import staticfiles
from paypalrestsdk import payments

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)%$4fwtv^bwoa838=)%2y*4n3-xhd%=k&hf#lgrq-bs1h6!=#5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'corsheaders',

    # Custom apps - use the AppConfig format
    'core.apps.CoreConfig',  # Instead of just 'core'
    'accounts.apps.AccountsConfig',
    'movies.apps.MoviesConfig',
    'portfolio.apps.PortfolioConfig',
    'workshops.apps.WorkshopsConfig',
    'payments.apps.PaymentsConfig',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'usanii_mtaani.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'usanii_mtaani.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Custom user model
AUTH_USER_MODEL = 'accounts.User'
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# Fixed configuration:
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Changed to a different directory
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Different from STATICFILES_DIRS
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}
# CORS settings
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Only in development
CORS_ALLOW_CREDENTIALS = True
# Session settings
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
# M-Pesa Configuration
MPESA_ENVIRONMENT = "sandbox"  # or "production"
MPESA_CONSUMER_KEY = os.environ.get("MPESA_CONSUMER_KEY", "your-consumer-key")
MPESA_CONSUMER_SECRET = os.environ.get("MPESA_CONSUMER_SECRET", "your-consumer-secret")
MPESA_SHORTCODE = os.environ.get("MPESA_SHORTCODE", "your-shortcode")
MPESA_PASSKEY = os.environ.get("MPESA_PASSKEY", "your-passkey")
# PayPal Configuration
PAYPAL_MODE = os.environ.get("PAYPAL_MODE", "sandbox")  # or "live"
PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID", "your-client-id")
PAYPAL_CLIENT_SECRET = os.environ.get("PAYPAL_CLIENT_SECRET", "your-client-secret")
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',  # Google
    'social_core.backends.facebook.FacebookOAuth2',  # Facebook
    'django.contrib.auth.backends.ModelBackend',  # Django default
)
# Social Auth settings
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/accounts/login/'
# Google OAuth2 settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'YOUR_GOOGLE_CLIENT_ID'  # Google Client ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'  # Google Client Secret
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']
# Facebook OAuth2 settings
SOCIAL_AUTH_FACEBOOK_KEY = 'YOUR_FACEBOOK_APP_ID'  # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'YOUR_FACEBOOK_APP_SECRET'  # Facebook App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}