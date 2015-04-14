# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.contrib.auth.models import UserManager
from datetime import datetime

# We need to create our own model manager,
# for some defaults to be set when creating an admin account from the command line.

class MemberUserManager(UserManager):
	def create_superuser(self, username, email, password):
		# This should be self explanatory. We set some defaults when creating an user. Only used when using the ./manage command for creating admins.
		user = self.model(username=username, email=email,
						  refreshedon=datetime.now(),
						  is_superuser=True,
						  is_administrator=True,
						  is_moderator=True,
						  is_staff=True,
						  is_active=True)
		user.set_password(password)
		user.save()