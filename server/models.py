# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.db import models
from member.models import Member
from django.core.urlresolvers import reverse
from server.groupapi.basemodel import GroupBaseModel

from autoslug import AutoSlugField

# This file is a description of the interface between the database and django.
# We don't do anything fancy in here, so the regular django manual should be sufficient~
# https://docs.djangoproject.com/en/1.8/topics/db/models/
# https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/

class Server(GroupBaseModel):
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

class Volunteer(models.Model):
	member = models.ForeignKey(Member)
	server = models.ForeignKey(Server)
	answer = models.TextField()
	role = models.CharField(max_length=200)
	
	def __str__(self):
		return self.server.name  + '/' + self.member.firstname + ' ' + self.member.surname
	
	STATUSCODES = (
	("OK", "Accepted"),
	("WAITING", "Waiting"),
	("DENIED", "Denied"),
	)
	
	#accepted = models.BooleanField(default=False)
	
	status = models.CharField(max_length=200, default="WAITING", choices=STATUSCODES)
	
	sec_edit = models.BooleanField(default=False)
	sec_accept = models.BooleanField(default=False)
	sec_moderator = models.BooleanField(default=False)
	
	createdon = models.DateTimeField('Created on', auto_now_add=True)
	
	@staticmethod
	def patch_user_moderator(user,server):
		is_server_moderator = False
		try:
			# And return if we find admin rights on the current user
			volun = Volunteer.objects.all().filter(member=user,server=server,status="OK")[0]
			if volun.sec_moderator:
				is_server_moderator = True
		except:
			pass	
		
		if is_server_moderator:
			user.is_moderator = True
			return user
	
	class Meta:
		ordering = ["-sec_accept", "-sec_edit", "role"]

class rocketchat(models.Model):
		server = models.ForeignKey(Server)
		channelname = models.CharField(max_length=200)
		rocketenabled = models.BooleanField(default=False)
