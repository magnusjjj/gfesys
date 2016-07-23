from django.contrib.contenttypes.models import ContentType
from django.contrib.sites import requests
from django.shortcuts import render, redirect

from profileapi.templatetags import profileurl
from profileapi.models import rocketchat, Volunteer
from profileapi.helpers.ProfileView import ProfileView
from guardian.shortcuts import assign_perm

# The view that adds or edits a profile
class EditProfile(ProfileView):
	def can_edit(self, profile, user):
		if user.is_administrator:
			return True
		if (profile.pk is None) and self.profilemodel.allow_add(user):
			return True
		if user.has_perm("edit", profile):
			return True
		return False

	def get(self, request, profile_id=0):
		# Fetch (or create) the profile
		if profile_id == 0:
			self.context["profile"] = self.profilemodel()
			if not self.can_edit(self.context["profile"], request.user):
				raise ValueError('You dont have access to this function. Boo!')
		else:
			self.context["profile"] = self.profilemodel.objects.get(pk=profile_id)
			if not request.user.has_perm("edit", self.context["profile"]):
				raise ValueError('You dont have access to this function. Boo!')

		self.context["profile_id"] = profile_id

		try:
			self.context["channels"] = rocketchat.objects.filter(profile=self.context["profile"])
		except:
			pass

		# And render
		return render(request, 'profileapi/edit.html', self.context)


	def post(self, request, profile_id="0"):
		# Fetch (or create) the profile
		if profile_id == "0":
			self.context["profile"] = self.profilemodel()
		else:
			self.context["profile"] = self.profilemodel.objects.get(pk=profile_id)

		content_type = ContentType.objects.get_for_model(self.context["profile"])

		if self.can_edit(self.context["profile"], request.user):
			# Modify the object
			self.context["profile"].name = request.POST["name"]
			self.context["profile"].description = request.POST["description"]

			if self.profilemodel.has_questions:
				self.context["profile"].questions = request.POST["questions"]

			if self.profilemodel.has_status:
				self.context["profile"].status = request.POST["status"]

			# Todo, handle errors here better:
			if 'image' in request.FILES:
				self.context["profile"].image = request.FILES['image']
			else:
				raise ValueError('You NEED to upload an image!')

			# Save the object
			self.context["profile"].save()

			if profile_id == "0":
				the_volunteer = Volunteer()
				the_volunteer.volunteer_for = self.context["profile"]
				the_volunteer.member = request.user
				the_volunteer.answer = ""
				the_volunteer.role = "Server Owner"
				the_volunteer.status = "OK"
				the_volunteer.save()

				assign_perm('volunteer_edit', request.user, self.context["profile"])
				assign_perm('add_page', request.user, self.context["profile"])
				assign_perm('edit_page', request.user, self.context["profile"])
				assign_perm('edit', request.user, self.context["profile"])
				assign_perm('moderate', request.user, self.context["profile"])

			rocketchannels = request.POST.getlist('rocketchannel')
			rocketchat.objects.filter(chatroom_for_object_id=self.context["profile"].pk,
									  chatroom_for_content_type=content_type).delete()

			for rocketchannel in rocketchannels:
				m = rocketchat()
				m.channelname = rocketchannel
				m.chatroom_for = self.context["profile"]
				if request.POST.get("rocketenabled", False) == "True":
					r = requests.post('http://chat.gfe.nu:1420/ChannelCreate',
									  json={"ChannelName": rocketchannel, "ServerName": self.context["profile"].name,
											"Enabled": "1"})
					m.rocketenabled = 1
				else:
					m.rocketenabled = 0
					r = requests.post('http://chat.gfe.nu:1420/ChannelCreate',
									  json={"ChannelName": rocketchannel, "ServerName": self.context["profile"].name,
											"Enabled": "0"})
				m.save()
			return redirect(profileurl.profileurl(self.context, 'edit', profile_id=self.context["profile"].id))
		else:
			raise ValueError('You dont have access to this function. Boo!')