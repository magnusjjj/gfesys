#!/usr/bin/python

# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

import sys
import random
import string
import os

class Installer:
	def pip_install():
		# Install all the python dependencies :)
		os.system("pip install -r requirements.txt")
	
	def installer_console_tutorial(self):
		# We generate the settings file. This function *looks* big and scary, but is really super duper simple. Watch:
		
		# Open the settings file for writing:
		fout = open("gfe/settings_local", "w")
		
		# Generate a naive security key for cookies and things:
		SECRET_KEY = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(20))
		
		# Get the current directory
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		
		# Get the directory to store all the static files in:
		STATIC_ROOT = os.path.join(BASE_DIR, 'static')
		
		# Get the directory to store all the media (image uploads, etc) in:
		MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
		
		# Ask the user a bunch of questions:
		
		print("What mail do you want to send emails from? ")
		EMAILFROM = sys.stdin.readline().strip()
		
		print("What is the database name? ")
		DATABASE_NAME = sys.stdin.readline().strip()
		
		print("What is the database user? ")
		DATABASE_USER = sys.stdin.readline().strip()
		
		print("What is the database password? ")
		DATABASE_PASSWORD = sys.stdin.readline().strip()
		
		print("What is the database host? ")
		DATABASE_HOST = sys.stdin.readline().strip()
		
		# Generate the string with the settings file in, yay!
		
		file = """
		SECRET_KEY = '"""+SECRET_KEY+"""'

		# SECURITY WARNING: don't run with debug turned on in production!
		DEBUG = True

		TEMPLATE_DEBUG = True

		ALLOWED_HOSTS = []

		DATABASES = {
			'default': {
				'ENGINE': 'django.db.backends.mysql',
				'NAME': '"""+DATABASE_NAME.encode("string_escape") +"""',
				'USER': '"""+DATABASE_USER.encode("string_escape") +"""',
				'PASSWORD': '"""+DATABASE_PASSWORD.encode("string_escape") +"""',
				'HOST': '"""+DATABASE_HOST.encode("string_escape") +"""'
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

		STATIC_URL = '/static/'
		STATIC_ROOT= '"""+ STATIC_ROOT.encode("string_escape") +"""'

		MEDIA_ROOT = '"""+ MEDIA_ROOT.encode("string_escape")  + """'
		MEDIA_URL = "/media/"

		EMAILFROM = '""" + EMAILFROM.encode("string_escape")  + """'
		"""
		
		# Save and close. Done!
		fout.write(file)
		fout.close()
		
		# That wasn't so bad, was it?
	
	def post_config():
		os.system("git update-index --assume-unchanged gfe/settings_local.py")
		# All the configuration *after* the settings have been saved
		os.system("./manage.py collectstatic")
		os.system("./manage.py createmigrations")
		os.system("./manage.py migrate")
		os.system("./manage.py createcachetable spirit_cache")

# Run the installer :)
installer = Installer()
installer.pip_install()
installer.installer_console_tutorial()
installer.post_config()
