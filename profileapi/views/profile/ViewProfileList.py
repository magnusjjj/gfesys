from django.shortcuts import render

from server.models import Server
from django.views.generic import View
from profileapi.helpers.ProfileView import ProfileView

# This should... probably not be here. Eheheheh. List of servers.
class ViewProfileList(ProfileView):
	def get(self, request):
		status_list = [Server.STATUS_LIVE, Server.STATUS_TESTING]
		if request.user.has_perm("server.VIEW_DRAFTS"):
			status_list.append(Server.STATUS_DRAFT)
		# Get all the servers, and order by id.
		if hasattr(self.profilemodel, "status"):
			self.context["profiles"] = self.profilemodel.objects.filter(status__in=status_list).order_by('status','id')
		else:
			self.context["profiles"] = self.profilemodel.objects.filter().order_by('status', 'id')
		# Render that thing right up. Hence why this should not not be here, but, alas, penis.
		return render(request,'servers/index.html', self.context)

