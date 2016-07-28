# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.db import models
import spirit.models.user
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractBaseUser
import spirit.models.user
from .memberusermanager import MemberUserManager
from django.utils.encoding import python_2_unicode_compatible

# This file is a description of the interface between the database and django.
# We do some slightly different stuff here, mainly importing Spirit (the forum engine) for the auth model.
# https://docs.djangoproject.com/en/1.8/topics/db/models/
# https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/

# This descriptor fixes __str__ on python2
@python_2_unicode_compatible
class Member(spirit.models.user.AbstractUser):
	objects = MemberUserManager()
	
	GravatarTypes = (('identicon', 'A geometric pattern based on an email hash'),
	('monsterid', "A generated 'monster' with different colors, faces, etc"),
	('wavatar', "Generated faces with differing features and backgrounds"),
	('retro', 'awesome generated, 8-bit arcade-style pixelated faces'))
	
	
	# This is the function that prints the 'presentation user name'.
	# If you want to change how the users look ("Magnus Johnsson") when you
	# use them like strings, here it is:
	def __str__(self):
		return self.username
	
	nick = models.CharField(max_length=200)
	birthdate = models.CharField(max_length=200)
	
	phone = models.CharField(max_length=200)
	mobile = models.CharField(max_length=200)
	
	street = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	country_id = CountryField()
	zip = models.CharField(max_length=200)
	careof = models.CharField(max_length=200)	
	socialsecuritynumber = models.CharField(max_length=200)
	
	joinedon = models.DateTimeField('Joined on', auto_now_add=True)
	refreshedon = models.DateTimeField('Refreshed on', null=True)
	
	image = models.ImageField(max_length=500, width_field='image_width', height_field='image_height', upload_to='members')
	image_height = models.IntegerField(default=0)
	image_width = models.IntegerField(default=0)
	
	is_opt_in = models.BooleanField(default=False)
	use_gravatar = models.BooleanField(default=False)
	gravatar_type = models.CharField(default='identicon', max_length=20, choices=GravatarTypes)
	
	membership_populated = models.BooleanField(default=True)
