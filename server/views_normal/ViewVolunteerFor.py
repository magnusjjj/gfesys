from django.shortcuts import render

from server.defaultview import DefaultView
from server.models import Server, Volunteer

# This view is used when a user wants to send in an application to become a volunteer
class ViewVolunteerFor(DefaultView):
	def get(self, request, server_id):
		super(ViewVolunteerFor, self).get(request)
		context = {}
		# Get the server in question
		context["server"] = Server.objects.get(pk=server_id)
		# Render it
		return render(request,'servers/volunteer.html', context)

	def post(self, request, server_id):
		super(ViewVolunteerFor, self).get(request)
		context = {}
		# Get the server in question
		context["server"] = Server.objects.get(pk=server_id)
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


