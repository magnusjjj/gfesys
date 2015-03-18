from django.db import models
from member.models import Member

class Server(models.Model):
	def __str__(self):
		return self.name
	name = models.CharField(max_length=200)
	
	description = models.TextField()
	howto = models.TextField()
	rules = models.TextField()
	questions = models.TextField()
	
	
	image = models.ImageField(max_length=500, width_field='image_width', height_field='image_height', upload_to='servers')
	image_height = models.IntegerField()
	image_width = models.IntegerField()

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
	
	createdon = models.DateTimeField('Created on', auto_now_add=True)
	
	class Meta:
		ordering = ["-sec_accept", "-sec_edit", "role"]
