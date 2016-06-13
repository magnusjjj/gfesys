from autoslug import AutoSlugField
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from member.models import Member

class ProfileTemplate(models.Model):
	def __str__(self):
		return self.name

	name = models.CharField(max_length=200)
	slug = AutoSlugField(max_length=40, populate_from='name')

	description = models.TextField()

	def get_absolute_url(self):
		return "You need to add a get_absolute_url to this model"

	image = models.ImageField(max_length=500, width_field='image_width', height_field='image_height', upload_to='profiles')
	image_height = models.IntegerField()
	image_width = models.IntegerField()


class rocketchat(models.Model):
	chatroom_for_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	chatroom_for_object_id = models.PositiveIntegerField()
	chatroom_for = GenericForeignKey('chatroom_for_object_id', 'chatroom_for_content_type')
	channelname = models.CharField(max_length=200)
	rocketenabled = models.BooleanField(default=False)


class Volunteer(models.Model):
	member = models.ForeignKey(Member)
	volunteer_for_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	volunteer_for_object_id = models.PositiveIntegerField()
	volunteer_for = GenericForeignKey('volunteer_for_object_id','volunteer_for_content_type')
	answer = models.TextField()
	role = models.CharField(max_length=200)

	def __str__(self):
		return self.server.name + '/' + self.member.firstname + ' ' + self.member.surname

	STATUSCODES = (
		("OK", "Accepted"),
		("WAITING", "Waiting"),
		("DENIED", "Denied"),
	)

	# accepted = models.BooleanField(default=False)

	status = models.CharField(max_length=200, default="WAITING", choices=STATUSCODES)

	sec_edit = models.BooleanField(default=False)
	sec_accept = models.BooleanField(default=False)
	sec_moderator = models.BooleanField(default=False)

	createdon = models.DateTimeField('Created on', auto_now_add=True)

	@staticmethod
	def patch_user_moderator(user, server):
		is_server_moderator = False
		try:
			# And return if we find admin rights on the current user
			volun = Volunteer.objects.all().filter(member=user, server=server, status="OK")[0]
			if volun.sec_moderator:
				is_server_moderator = True
		except:
			pass

		if is_server_moderator:
			user.is_moderator = True
			return user

	class Meta:
		ordering = ["-sec_accept", "-sec_edit", "role"]
