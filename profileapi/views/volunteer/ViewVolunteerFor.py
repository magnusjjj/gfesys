from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from profileapi.models import Volunteer
from profileapi.helpers.ProfileView import ProfileView

# This view is used when a user wants to send in an application to become a volunteer
class ViewVolunteerFor(ProfileView):
	def get(self, request, profile_id):
		# Get the server in question
		self.context["profile"] = self.profilemodel.objects.get(pk=profile_id)
		# Render it
		return render(request,'profileapi/volunteer.html', self.context)

	def post(self, request, profile_id):
		# Get the server in question
		self.context["server"] = self.profilemodel.objects.get(pk=profile_id)
		# Display a shiny message
		self.context["hasposted"] = True

		# Create and save a volunteer
		vol = Volunteer.objects.create(
			member = request.user,
			volunteer_for_object_id = self.context["profile"].pk,
			volunteer_for_content_type=ContentType.objects.get_for_model(self.context["profile"]),
			answer = request.POST["answer"],
			role = "",
		)

		vol.save()

		# Render. Wooooo.
		return render(request,'profileapi/volunteer.html', self.context)


