from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from page.models import Page
from profileapi.models import Volunteer
from profileapi.helpers.ProfileView import ProfileView

# This view is for viewing a specific profile

class ViewProfile(ProfileView):
	profilemodel = None

	def get(self, request, slug, slug_page=None):
		# Get the profile in question
		self.context["profile"] = self.profilemodel.objects.get(slug=slug)
		self.context["request"] = request

		# Get a list of text pages for this server
		self.context["pages"] = Page.objects.filter(parent_object_id=self.context["profile"].pk,
									parent_content_type=ContentType.objects.get_for_model(self.context["profile"]))
		# What page is active?
		if slug_page is None:
			try:
				self.context["page_active"] = self.context["pages"][0].slug
			except:
				self.context["page_active"] = ""
		else:
			self.context["page_active"] = slug_page

		# Get a list of volunteers for the server
		self.context["volunteers"] = Volunteer.objects.all().filter(volunteer_for_object_id=self.context["profile"].pk,
								volunteer_for_content_type=ContentType.objects.get_for_model(self.context["profile"]),
								status="OK")
		try:
			Volunteer.objects.get(volunteer_for_object_id=self.context["profile"].pk,
										   volunteer_for_content_type=ContentType.objects.get_for_model(
											self.context["profile"]),
										   status="OK", member=request.user)
			self.context["is_volunteer"] = True
		except:
			self.context["is_volunteer"] = False


		self.context["has_volunteer_edit"] = request.user.has_perm("volunteer_edit", self.context["profile"])
		self.context["has_page_edit"] = request.user.has_perm("edit_page",self.context["profile"])

		# And, BAM, render that thing.
		return render(request,'profileapi/detail.html', self.context)

