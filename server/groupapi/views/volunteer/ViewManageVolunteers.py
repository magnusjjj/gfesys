from django.shortcuts import render

from server.defaultview import DefaultView
from server.models import Server, Volunteer

# This view is for an admin, allowing them to manage the list of volunteers
class ViewManageVolunteers(DefaultView):
	def get(self, request, server_id):
		super(ViewManageVolunteers, self).get(request)
		context = {}
		# Get the server in question
		context["server"] = Server.objects.get(pk=server_id)
		# Find out if we have editing rights to said server
		self.setrights_server(request, context, server_id)
		# Get the list of volunteers...
		context["applicants"] = Volunteer.objects.filter(server=context["server"])
		# Now render it. So hard.
		return render(request,'servers/managevolunteers.html', context)

