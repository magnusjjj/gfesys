from django.shortcuts import render, redirect

from page import views
from page.models import Page
from server.defaultview import DefaultView
from server.models import Server
from server.views_normal.StripSettings import StripSettings


class AddPage(DefaultView):
	def get(self, request, server_id):
		super(AddPage, self).get(request)
		context = {}
		# Fetch the server
		context["server"] = Server.objects.get(pk=server_id)

		# Empty page, for the view
		page = Page()
		context["page"] = page

		# Fetch our access rights
		self.setrights_server(request, context, server_id)

		# Security sanity check that we have edit rights
		if request.user.is_administrator or context["volunteer"].sec_edit:
			# Some sort of wierd error causes the request to point to the wrong place. What?
			context["request"] = request
			return render(request,'servers/addpage.html', context)

	def post(self, request, server_id):
		super(AddPage, self).get(request)
		server = Server.objects.get(pk=server_id)
		context = {}
		# Fetch the server
		context["server"] = Server.objects.get(pk=server_id)

		# Fetch our access rights
		self.setrights_server(request, context, server_id)

		# Security sanity check that we have edit rights
		if request.user.is_administrator or context["volunteer"].sec_edit:
			# Some sort of wierd error causes the request to point to the wrong place. What?
			context["request"] = request
			strip = StripSettings()
			page = views.handle_save(request, None, server, strip)
			return redirect(server)