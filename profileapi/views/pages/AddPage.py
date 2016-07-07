from django.shortcuts import render, redirect

from page import views
from page.models import Page
from StripSettings import StripSettings

from profileapi.helpers.ProfileView import ProfileView

class AddPage(ProfileView):
	def get(self, request, profile_id):
		# Fetch the profile
		self.context["profile"] = self.profilemodel.objects.get(pk=profile_id)

		# Empty page, for the view
		page = Page()
		self.context["page"] = page

		# Security sanity check that we have edit rights
		if request.user.has_perm("profileapi.add_page", self.context["profile"]):
			# Some sort of wierd error causes the request to point to the wrong place. What?
			self.context["request"] = request
			return render(request,'profileapi/addpage.html', self.context)

	def post(self, request, profile_id):
		self.context["profile"] = self.profilemodel.objects.get(pk=profile_id)

		# Security sanity check that we have edit rights
		if request.user.has_perm("profileapi.edit_page", self.context["profile"]):
			# Some sort of wierd error causes the request to point to the wrong place. What?
			self.context["request"] = request
			strip = StripSettings()
			page = views.handle_save(request, None, self.context["profile"], strip)
			return redirect(self.context["profile"])