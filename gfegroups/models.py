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

class GfeGroup(ProfileTemplate):
	modelname = "Group"
	joinbuttonname = "Join this Group!"
	volunteername = "Member"

	def get_absolute_url(self):
		return reverse('gfegroups:profile:detail', args=[str(self.slug)])

	@staticmethod
	def allow_add(user):
		if user.is_anonymous():
			return False
		else:
			return True

	class Meta:
		permissions = (
			('volunteer_edit', 'Manage volunteers'),
			('add_page', 'Add page'),
			('edit_page', 'Edit page'),
			('edit', 'Edit'),
			('moderate', 'Moderate'),
			('view_drafts', 'Viev draft profiles'),
			('can_add', 'Can add profiles'),
		)