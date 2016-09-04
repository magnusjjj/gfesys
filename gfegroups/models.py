# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.core.urlresolvers import reverse
from django.db import models


from profileapi.models import ProfileTemplate



class GfeGroup(ProfileTemplate):
	# modelname, joinbuttonname, and volunteername are all translations that you use in the templates.
	#For instance, if you in the template do a 'This is  a list of all our {{profile.modelname}}s',
	#that will type out 'This is a list of all our Groups'
	modelname = "Group"
	joinbuttonname = "Join this Group!"
	volunteername = "Member"

	# This function says what url to return if we do {{ profile.get_absolute_url }} in the template
	def get_absolute_url(self):
		return reverse('gfegroups:profile:detail', args=[str(self.slug)])

	# This function, right here, says whether or not a user has the right to *create* a new group.
	# Current policy is to allow anybody that is logged in to create new groups.
	# This is where you might, at a future date, add something like a limit on the amount of groups a user is allowed
	# to create.
	@staticmethod
	def allow_add(user):
		if user.is_anonymous():
			return False
		else:
			return True

	# For some reason, we need to add this list of permissions on every submodel of ProfileTemplate. Go figure.
	# Basically, its a list of permissions that you can have that relates to this model.
	# For instance, you can have the permission 'volunteer_edit' on a group, and that lets you edit
	# the group members permissions.
	# Todo: Make a.. meta class to inherit from? :P

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