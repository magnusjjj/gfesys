import requests
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect

from profileapi.templatetags import profileurl
from server.models import Server
from profileapi.models import rocketchat
from django.views.generic import View
from profileapi.helpers.ProfileView import ProfileView


# This is the motherload. The actual view that saves the server info.
class UpdateProfile(ProfileView):
	def post(self, request, profile_id="0"):
		# Fetch (or create) the server
		if profile_id == "0":
			self.context["profile"] = self.profilemodel()
		else:
			self.context["profile"] = self.profilemodel.objects.get(pk=profile_id)

		content_type = ContentType.objects.get_for_model(self.context["profile"])

		if request.user.has_perm("profileapi.edit", self.context["profile"]):
			# Modify the object
			self.context["profile"].name = request.POST["name"]
			self.context["profile"].description = request.POST["description"]
			self.context["profile"].questions = request.POST["questions"]

			if request.POST["status"]:
				self.context["profile"].status = request.POST["status"]

			# Todo, handle errors here better:
			if 'image' in request.FILES:
				self.context["profile"].image = request.FILES['image']

			# Save the object
			self.context["profile"].save()

			rocketchannels = request.POST.getlist('rocketchannel')
			rocketchat.objects.filter(chatroom_for_object_id=self.context["profile"].pk, chatroom_for_content_type=content_type).delete()

			for rocketchannel in rocketchannels:
				m = rocketchat()
				m.channelname = rocketchannel
				m.server = self.context["profile"]
				if request.POST.get("rocketenabled", False) == "True":
					r = requests.post('http://chat.gfe.nu:1420/ChannelCreate', json={"ChannelName": rocketchannel, "ServerName": self.context["profile"].name, "Enabled": "1"})
					m.rocketenabled = 1
				else:
					m.rocketenabled = 0
					r = requests.post('http://chat.gfe.nu:1420/ChannelCreate', json={"ChannelName": rocketchannel, "ServerName": self.context["profile"].name, "Enabled": "0"})
				m.save()

				return redirect(profileurl.profileurl(self.context, 'edit', profile_id=self.context["profile"].id))

