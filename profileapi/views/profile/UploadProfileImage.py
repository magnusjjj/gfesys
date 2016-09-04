from django.shortcuts import redirect
from profileapi.helpers.ProfileView import ProfileView
class UploadProfileImage(ProfileView):
	def post(self, request, profile_id):
		# Fetch the server
		self.context["profile"] = self.profilemodel.objects.get(pk=profile_id)

		# Security sanity check that we have edit rights
		if request.user.has_perm("edit", self.context["profile"]):
			# Handle the image upload
			self.context["profile"].image = request.FILES['image']
			self.context["profile"].save()
			return redirect("editserver", profile_id)