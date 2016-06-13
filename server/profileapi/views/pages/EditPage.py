from django.shortcuts import render, redirect

from page import views
from page.models import Page
from server.defaultview import DefaultView
from server.profileapi.views.pages.StripSettings import StripSettings
from server.models import Server


class EditPage(DefaultView):
	def get(self, request, page_id):
		super(EditPage, self).get(request)
		context = {}
		# Fetch Page
		page = Page.objects.get(pk=page_id)
		context["page"] = page

		if type(page.parent) is Server:
			# Fetch the server
			context["server"] = page.parent

			# Fetch our access rights
			self.setrights_server(request, context, page.parent.pk)

			# Security sanity check that we have edit rights
			if request.user.is_administrator or context["volunteer"].sec_edit:
				return render(request,'servers/addpage.html', context)

	def post(self, request, page_id):
		super(EditPage, self).get(request)
		context = {}
		# Fetch Page
		page = Page.objects.get(pk=page_id)
		context["page"] = page

		if type(page.parent) is Server:
			# Fetch the server
			context["server"] = page.parent

			# Fetch our access rights
			self.setrights_server(request, context, page.parent.pk)
			strip = StripSettings()

			# Security sanity check that we have edit rights
			if request.user.is_administrator or context["volunteer"].sec_edit:
				page = views.handle_save(request, page_id, context["server"], strip)
				return redirect(context["server"])