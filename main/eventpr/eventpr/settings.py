"""
Django settings for eventpr project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-62%&ldh=ror7t@+^m(hxpq6mrd=ammgc@e6o^k7v(27_-t!5*a"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [


    #'paymentapp',
    'eventapp',
    'userapp',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

ROOT_URLCONF = "eventpr.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "eventpr.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Add this line

MEDIA_ROOT = BASE_DIR / 'pic'
MEDIA_URL = '/media/'
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# Enable caching headers for static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Cache timeout (set as per your preference)
STATIC_CACHE_TIMEOUT = 86400  # 1 day (in seconds), can adjust this

# unauth user redirect
LOGIN_URL = '/user/login/'
LOGIN_REDIRECT_URL = '/' 
LOGOUT_REDIRECT_URL = '/' 

# Email configuration for notifications



EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587  # TLS port
EMAIL_USE_TLS = True  # TLS must be enabled
EMAIL_HOST_USER = 'eventpro49@gmail.com'
EMAIL_HOST_PASSWORD = 'dpodrpzmufxecwny'  # Make sure this is the correct app password
DEFAULT_FROM_EMAIL = 'eventpro49@gmail.com'
ADMIN_EMAIL = 'amal183626@gmail.com'  # or the actual admin email

AUTH_USER_MODEL = 'userapp.CustomUser'

