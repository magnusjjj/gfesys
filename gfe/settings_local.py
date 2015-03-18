# SECURITY WARNING: keep the secret key used in production secret!
# There is a neat app for this at:
# http://www.miniwebtool.com/django-secret-key-generator/
# CHANGE HERE:

SECRET_KEY = ''

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

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

STATIC_URL = '/static/'
STATIC_ROOT= "/home/django/gfesys/static/"

MEDIA_ROOT = "/home/django/gfesys/media/"
MEDIA_URL = "/media/"

EMAILFROM = "noreply@tuxie.se"

