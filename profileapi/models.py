from autoslug import AutoSlugField
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from member.models import Member

class ProfileTemplate(models.Model):
	modelname = "ProfileTemplate. Set this, ffs, in your model."
	has_questions = False
	has_status = False
	volunteername = "Membername. Set this, ffs, in your model."
	joinbuttonname = "Join this, mothatrucker"

	@staticmethod
	def allow_add(user):
		if user.is_administrator:
			return True
		else:
			return False

	def __str__(self):
		return self.name

	name = models.CharField(max_length=200)
	slug = AutoSlugField(max_length=40, populate_from='name', unique=True)

	description = models.TextField()

	def get_absolute_url(self):
		return "You need to add a get_absolute_url to this model"

	image = models.ImageField(max_length=500, width_field='image_width', height_field='image_height', upload_to='profiles')
	image_height = models.IntegerField()
	image_width = models.IntegerField()

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

class rocketchat(models.Model):
	chatroom_for_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	chatroom_for_object_id = models.PositiveIntegerField()
	chatroom_for = GenericForeignKey('chatroom_for_content_type', 'chatroom_for_object_id')
	channelname = models.CharField(max_length=200)
	rocketenabled = models.BooleanField(default=False)


class Volunteer(models.Model):
	member = models.ForeignKey(Member)
	volunteer_for_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	volunteer_for_object_id = models.PositiveIntegerField()
	volunteer_for = GenericForeignKey('volunteer_for_content_type','volunteer_for_object_id')
	answer = models.TextField()
	role = models.CharField(max_length=200)

	def __str__(self):
		return str(self.member)

	STATUSCODES = (
		("OK", "Accepted"),
		("WAITING", "Waiting"),
		("DENIED", "Denied"),
	)

	# accepted = models.BooleanField(default=False)

	status = models.CharField(max_length=200, default="WAITING", choices=STATUSCODES)

	createdon = models.DateTimeField('Created on', auto_now_add=True)

	@staticmethod
	def patch_user_moderator(user, profile):
		# And return if we find admin rights on the current user
		if user.has_perm('moderate', profile):
			user.is_moderator = True
		return user

	class Meta:
		ordering = ["role"]
