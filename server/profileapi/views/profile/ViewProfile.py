from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from page.models import Page
from server.models import Server
from server.profileapi.models import Volunteer
from django.views.generic import View

# This view is for viewing a specific server

class ViewDetail(View):
	def get(self, request, slug, slug_page=None):
		super(ViewDetail, self).get(request)
		context = {}
		# Get the server in question
		context["server"] = Server.objects.get(slug=slug)

		# Find out if we have editing rights to said server
		self.setrights_server(request, context, context["server"].pk)
		context["request"] = request

		# Get a list of text pages for this server
		context["pages"] = Page.objects.filter(parent_object_id=context["server"].pk,
									parent_content_type=ContentType.objects.get_for_model(context["server"]))
		# What page is active?
		if slug_page is None:
			try:
				context["page_active"] = context["pages"][0].slug
			except:
				context["page_active"] = ""
		else:
			context["page_active"] = slug_page

		# Get a list of volunteers for the server
		context["volunteers"] = Volunteer.objects.all().filter(server=context["server"],status="OK")
		# And, BAM, render that thing.
		return render(request,'servers/detail.html', context)

