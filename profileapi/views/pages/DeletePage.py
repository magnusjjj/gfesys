from profileapi.helpers.ProfileView import ProfileView
from profileapi.models import ProfileTemplate

from django.shortcuts import redirect

from page.models import Page
from django.views.generic import View

class DeletePage(ProfileView):
	def get(self, request, page_id):
		# Fetch Page
		page = Page.objects.get(pk=page_id)

		if issubclass(type(page.parent), ProfileTemplate):
			# Fetch the profile
			self.context["profile"] = page.parent

			# Security sanity check that we have edit rights
			if request.user.has_perm("delete_page", page):
				page.delete()
				return redirect(page.parent)