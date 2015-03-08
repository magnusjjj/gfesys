from django.db import models
from django_countries.fields import CountryField

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


class Member(models.Model):
	def __str__(self):
		nicky = " " if self.nick == "" else " \"" + self.nick +  "\" "
		return self.firstname + nicky + self.surname
	
	firstname = models.CharField(max_length=200)
	surname = models.CharField(max_length=200)
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
	email = models.EmailField(max_length=254, unique=True)
	
	joinedon = models.DateTimeField('Joined on', auto_now_add=True)
	refreshedon = models.DateTimeField('Refreshed on')
	
	image = models.ImageField(max_length=500, width_field='image_width', height_field='image_height', upload_to='members')
	image_height = models.IntegerField()
	image_width = models.IntegerField()
	
	password_hash = models.CharField(max_length=200)
	password_salt = models.CharField(max_length=200) 

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
