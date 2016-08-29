from django.shortcuts import render, redirect
from django.views.generic import View

from page import views
from page.models import Page
from StripSettings import StripSettings
from profileapi.models import ProfileTemplate
from profileapi.helpers.ProfileView import ProfileView

class EditPage(ProfileView):
	def get(self, request, page_id):
		# Fetch Page
		page = Page.objects.get(pk=page_id)
		self.context["page"] = page

		if issubclass(type(page.parent), ProfileTemplate):
			# Fetch the profile
			self.context["profile"] = page.parent

			# Security sanity check that we have edit rights
			if request.user.has_perm("edit_page", page):
				return render(request,'profileapi/addpage.html', self.context)

	def post(self, request, page_id):
		# Fetch Page
		page = Page.objects.get(pk=page_id)
		self.context["page"] = page

		if issubclass(type(page.parent), ProfileTemplate):
			# Fetch the profile
			self.context["profile"] = page.parent

			strip = StripSettings()

			# Security sanity check that we have edit rights
			if request.user.has_perm("edit_page", page):
				page = views.handle_save(request, page_id, self.context["profile"], strip)
				return redirect(self.context["profile"])