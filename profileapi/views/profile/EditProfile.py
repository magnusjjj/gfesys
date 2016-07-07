from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect

from profileapi.templatetags import profileurl
from server.models import Server
from profileapi.models import rocketchat
from django.views.generic import View
from profileapi.helpers.ProfileView import ProfileView

# Simply the view that *renders* the edit screen
class EditProfile(ProfileView):
	def get(self, request, profile_id=0):
		# Fetch (or create) the profile
		if profile_id == 0:
			self.context["profile"] = self.profilemodel()
			if not request.user.has_perm("profileapi.can_add"):
				raise ValueError('You dont have access to this function. Boo!')
		else:
			self.context["profile"] = self.profilemodel.objects.get(pk=profile_id)

			if not request.user.has_perm("profileapi.edit", self.context["profile"]):
				raise ValueError('You dont have access to this function. Boo!')
		self.context["profile_id"] = profile_id
		try:
			self.context["channels"] = rocketchat.objects.filter(profile=self.context["profile"])
		except:
			pass
		# And render
		if request.user.has_perm("profileapi.edit", self.context["profile"]):
			return redirect(profileurl.profileurl(self.context, 'edit', profile_id=self.context["profile"].id))

