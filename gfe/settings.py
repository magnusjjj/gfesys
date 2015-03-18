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
from settings_local import *
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition

INSTALLED_APPS = ('server', 'member', 'page') + INSTALLED_APPS

TEMPLATE_CONTEXT_PROCESSORS += ("server.context.context",)

ROOT_URLCONF = 'gfe.urls'

WSGI_APPLICATION = 'gfe.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

AUTH_USER_MODEL = "member.Member"
