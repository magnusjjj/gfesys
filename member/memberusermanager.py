from django.contrib.auth.models import UserManager
from datetime import datetime

class MemberUserManager(UserManager):
	def create_superuser(self, username, email, password):
		user = self.model(username=username, email=email,
						  refreshedon=datetime.now(),
						  is_superuser=True,
						  is_administrator=True,
						  is_moderator=True,
						  is_staff=True,
						  is_active=True)
		user.set_password(password)
		user.save()