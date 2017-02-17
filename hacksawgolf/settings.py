"""
Django settings for hacksawgolf project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
with open('/projects/hacksawgolf/security/variables/secret_key.txt') as secret_key_file:
    SECRET_KEY = secret_key_file.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = ['127.0.0.1']

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    '.hacksawgolf.com',
    '.hacksawgolf.com.'
]

# Templates path
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'login',
    'register',
    'home',
    'golfer',
    'tournament',
    'team',
    'league',
    'rules'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hacksawgolf.urls'

WSGI_APPLICATION = 'hacksawgolf.wsgi.application'


# Database
with open('/projects/hacksawgolf/security/variables/mysql_pw.txt') as mysql_pw_file:
    MYSQL_PW = mysql_pw_file.read().strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hacksa5_hacksawgolf',
        'USER': 'hacksa5_webuser',
        'PASSWORD': MYSQL_PW,
        'HOST': '127.0.0.1'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/projects/hacksawgolf/hacksawgolf/hacksawgolf/'

# Static files paths
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), 'static')
),

# session settings
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
# session expire at 2 days (in seconds)
SESSION_COOKIE_AGE =  172800

with open('/projects/hacksawgolf/security/variables/email_pw.txt') as email_pw_file:
    EMAIL_PW = email_pw_file.read().strip()

# email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.hacksawgolf.com'
EMAIL_HOST_USER = 'ben@hacksawgolf.com'
EMAIL_HOST_PASSWORD = EMAIL_PW
EMAIL_PORT = 25

# tinymce settings
TINYMCE_JS_URL = os.path.join(STATIC_URL, "admin/js/tinymce/tinymce.min.js")
TINYMCE_JS_ROOT = os.path.join(STATIC_URL, "admin/js/tinymce/")
TINYMCE_DEFAULT_CONFIG = {
    'theme': "modern"
}