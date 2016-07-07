from django.shortcuts import render

from server.models import Server
from profileapi.models import Volunteer
from django.views.generic import View
from profileapi.helpers.ProfileView import ProfileView

# This view is used when a user wants to send in an application to become a volunteer
class ViewVolunteerFor(ProfileView):
	def get(self, request, profile_id):
		context = {}
		# Get the server in question
		context["server"] = Server.objects.get(pk=profile_id)
		# Render it
		return render(request,'servers/volunteer.html', context)

	def post(self, request, profile_id):
		context = {}
		# Get the server in question
		context["server"] = Server.objects.get(pk=profile_id)
		# Display a shiny message
		context["hasposted"] = True

		# Create and save a volunteer
		vol = Volunteer.objects.create(
			member = request.user,
			server = context["server"],
			answer = request.POST["answer"],
			role = "",
		)

		vol.save()

		# Render. Wooooo.
		return render(request,'servers/volunteer.html', context)


