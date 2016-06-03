from django.shortcuts import render

from server.defaultview import DefaultView
from server.models import Server
from server.views_normal.ViewIndex import ViewIndex


class ViewServerList(DefaultView):
	def get(self, request):
		super(ViewIndex, self).get(request)
		context = {}
		status_list = [Server.STATUS_LIVE, Server.STATUS_TESTING]
		if hasattr(request.user, 'is_administrator') and request.user.is_administrator:
			status_list.append(Server.STATUS_DRAFT)
		# Get all the servers, and order by id.
		context["servers"] = Server.objects.filter(status__in=status_list).order_by('status','id')
		# Render that thing right up
		return render(request,'servers/index.html', context)

