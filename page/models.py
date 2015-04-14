# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

# This file is a description of the interface between the database and django.
# We don't do anything fancy in here, so the regular django manual should be sufficient~
# https://docs.djangoproject.com/en/1.8/topics/db/models/
# https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/

class Page(models.Model):
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('page.views.page', args=[str(self.id)])
	
	name = models.CharField(max_length=200)
	content = models.TextField()
	type= models.CharField(max_length=200, default="")
	
	parent_content_type = models.ForeignKey(ContentType, blank=True, null=True)
	parent_object_id = models.PositiveIntegerField(blank=True, null=True)
	
	parent = GenericForeignKey('parent_content_type', 'parent_object_id')