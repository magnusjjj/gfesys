"""
Django settings for gfe project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from spirit.settings import *
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# There is a neat app for this at:
# http://www.miniwebtool.com/django-secret-key-generator/
# CHANGE HERE:

SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []




# Application definition

INSTALLED_APPS = ('server', 'member', 'page') + INSTALLED_APPS

TEMPLATE_CONTEXT_PROCESSORS += ("server.context.context",)

ROOT_URLCONF = 'gfe.urls'

WSGI_APPLICATION = 'gfe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# CHANGE HERE:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database name',
	'USER': 'database user',
	'PASSWORD': 'database password',
	'HOST': 'database host'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# CHANGE HERE:

STATIC_URL = '/static/'
STATIC_ROOT= "/home/django/gfe/static/"

MEDIA_ROOT = "/home/django/gfe/media/"
MEDIA_URL = "/media/"

EMAILFROM = "noreply@tuxie.se"

AUTH_USER_MODEL = "member.Member"
