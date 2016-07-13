from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.views.generic import View

from profileapi.models import Volunteer
from server.models import Server
from profileapi.helpers.ProfileView import ProfileView

# This view is for an admin, allowing them to manage the list of volunteers
class ViewManageVolunteers(ProfileView):
	def get(self, request, profile_id):
		# Get the profile in question
		self.context["profile"] = Server.objects.get(pk=profile_id)
		# Get the list of volunteers...
		self.context["applicants"] = Volunteer.objects.filter(
			volunteer_for_content_type=ContentType.objects.get_for_model(self.context["profile"]),
			volunteer_for_object_id=self.context["profile"].pk)
		# Now render it. So hard.
		return render(request,'profileapi/managevolunteers.html', self.context)

