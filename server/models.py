# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.core.urlresolvers import reverse
from django.db import models


from profileapi.models import ProfileTemplate

# This file is a description of the interface between the database and django.
# We don't do anything fancy in here, so the regular django manual should be sufficient~
# https://docs.djangoproject.com/en/1.8/topics/db/models/
# https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/

class Server(ProfileTemplate):
	questions = models.TextField()
	
	STATUS_LIVE = 1
	STATUS_TESTING = 2
	STATUS_DRAFT = 3
	
	STATUS_CHOICES = (
		(STATUS_LIVE, 'Live'),
		(STATUS_TESTING, 'Testing'),
		(STATUS_DRAFT, 'Draft'),
	)
	
	def get_absolute_url(self):
		return reverse('server:detail', args=[str(self.slug)])

	status = models.IntegerField(choices=STATUS_CHOICES, default=3)


