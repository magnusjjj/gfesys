from django.db import models
import spirit.models.user
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractBaseUser
import spirit.models.user
# Create your models here.
class Member(spirit.models.user.AbstractUser):
	def __str__(self):
		nicky = " " if self.nick == "" else " \"" + self.nick +  "\" "
		return self.first_name + nicky + self.last_name
	
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
	
	joinedon = models.DateTimeField('Joined on', auto_now_add=True)
	refreshedon = models.DateTimeField('Refreshed on')
	
	image = models.ImageField(max_length=500, width_field='image_width', height_field='image_height', upload_to='members')
	image_height = models.IntegerField()
	image_width = models.IntegerField()

	is_opt_in = models.BooleanField(default=False)