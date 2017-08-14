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
	# modelname, joinbuttonname, and volunteername are all translations that you use in the templates.
	#For instance, if you in the template do a 'This is  a list of all our {{profile.modelname}}s',
	#that will type out 'This is a list of all our Groups'
	modelname = "Server"
	joinbuttonname = "Volunteer for this server!"
	volunteername = "Volunteer"

	# Signaling the profileapi to show the 'questions' when applying to be a volunteer,
	# and 'status' of the server on the edit page.
	has_questions = True
	has_status = True


	# This is the questions shown when applying to become a volunteer
	questions = models.TextField()

	# This is the whole status mcbob, shows whether or not the server is in live/testing/draft
	STATUS_LIVE = 1
	STATUS_TESTING = 2
	STATUS_DRAFT = 3
	
	STATUS_CHOICES = (
		(STATUS_LIVE, 'Live'),
		(STATUS_TESTING, 'Testing'),
		(STATUS_DRAFT, 'Draft'),
	)

	status = models.IntegerField(choices=STATUS_CHOICES, default=3)

	# This function says what url to return if we do {{ profile.get_absolute_url }} in the template
	def get_absolute_url(self):
		return reverse('server_profile:detail', args=[str(self.slug)])

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