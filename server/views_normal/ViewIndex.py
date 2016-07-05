from server.models import Server
from newsletter.models import Submission
from django.views.generic import View
from django.shortcuts import render
from profileapi.helpers.ProfileView import ProfileView

# This view is for the listing of all the servers

class ViewIndex(ProfileView):
	def get(self, request):
		status_list = [Server.STATUS_LIVE, Server.STATUS_TESTING]
		if hasattr(request.user, 'is_administrator') and request.user.is_administrator:
			status_list.append(Server.STATUS_DRAFT)
		# Get all the servers, and order by id.
		self.context["servers"] = Server.objects.filter(status__in=status_list).order_by('status','id')

		self.context["news"] = Submission.objects.filter(publish=True)

		# Render that thing right up
		return render(request,'servers/index.html', self.context)