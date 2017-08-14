# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from .memberusermanager import MemberUserManager
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from autoslug import AutoSlugField
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

# This file is a description of the interface between the database and django.
# We do some slightly different stuff here, mainly importing Spirit (the forum engine) for the auth model.
# https://docs.djangoproject.com/en/1.8/topics/db/models/
# https://docs.djangoproject.com/en/dev/ref/contrib/contenttypes/

# This descriptor fixes __str__ on python2

# Holy shit, the Spirit upgrade deprecated the entire user model. Ffffuuuck.
# So we, uhm.. copy pasted everything. Heres hoping for the best.
@python_2_unicode_compatible
class Member(AbstractUser):
	objects = MemberUserManager()
	
	username = models.CharField(_("username"), max_length=254, unique=True, db_index=True)
	first_name = models.CharField(_("first name"), max_length=30, blank=True)
	last_name = models.CharField(_("last name"), max_length=30, blank=True)
	email = models.EmailField(_("email"), max_length=254, unique=True)
	is_staff = models.BooleanField(_('staff status'), default=False,
								   help_text=_('Designates whether the user can log into this admin '
											   'site.'))
	is_active = models.BooleanField(_('active'), default=True,
									help_text=_('Designates whether this user should be treated as '
												'active. Unselect this instead of deleting accounts.'))
	
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	slug = AutoSlugField(populate_from="username", db_index=False, blank=True)
	is_verified = models.BooleanField(_('verified'), default=False,
									  help_text=_('Designates whether the user has verified his '
												  'account by email or by other means. Un-select this '
												  'to let the user activate his account.'))

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', ]
	
	def get_absolute_url(self):
		return reverse('spirit:profile-detail', kwargs={'pk': self.pk,
														'slug': self.slug})
	def email_user(self, subject, message, from_email=None):
		send_mail(subject, message, from_email, [self.email, ])
	
	GravatarTypes = (('identicon', 'A geometric pattern based on an email hash'),
	('monsterid', "A generated 'monster' with different colors, faces, etc"),
	('wavatar', "Generated faces with differing features and backgrounds"),
	('retro', 'awesome generated, 8-bit arcade-style pixelated faces'))
	
	
	# This is the function that prints the 'presentation user name'.
	# If you want to change how the users look ("Magnus Johnsson") when you
	# use them like strings, here it is:
	def __str__(self):
		return self.username
	
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
	refreshedon = models.DateTimeField('Refreshed on', null=True)
	
	image = models.ImageField(max_length=500, width_field='image_width', height_field='image_height', upload_to='members')
	image_height = models.IntegerField(default=0)
	image_width = models.IntegerField(default=0)
	
	is_opt_in = models.BooleanField(default=False)
	use_gravatar = models.BooleanField(default=False)
	gravatar_type = models.CharField(default='identicon', max_length=20, choices=GravatarTypes)
	
	membership_populated = models.BooleanField(default=True)

	def get_full_name(self):
		full_name = '' #  '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return ''