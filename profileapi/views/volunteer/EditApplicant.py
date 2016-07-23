from django.http import JsonResponse

from profileapi.models import Volunteer
from django.views.generic import View
from profileapi.helpers.ProfileView import ProfileView
from guardian.models import UserObjectPermission

from guardian.shortcuts import assign_perm, remove_perm

# This is a view to save changes to a volunteer, for the profile admins to use. AJAX, responds with a JSON string.
class EditApplicant(ProfileView):
	def post(self, request):
		# Fetch the volunteer
		applicant = Volunteer.objects.get(pk=int(request.POST["applicant_id"]))

		# A simple list to hold error messages in
		errors = []

		# And a dictionary to hold stuff to put in the JSON-response in
		vals = {}

		# Sanity check that we have editing rights
		if not request.user.has_perm("volunteer_edit", applicant.volunteer_for):
			errors.push("You don't have access to this command")
		else:
			# Edit the values requested:
			if "role" in request.POST:
				applicant.role = request.POST["role"]

			if "sec_accept" in request.POST:
				if request.POST["sec_accept"] == "true":
					assign_perm('volunteer_edit', applicant.member, applicant.volunteer_for)
				else:
					remove_perm('volunteer_edit', applicant.member, applicant.volunteer_for)

			if "sec_edit" in request.POST:
				if request.POST["sec_edit"] == "true":
					assign_perm('add_page', applicant.member, applicant.volunteer_for)
					assign_perm('edit_page', applicant.member, applicant.volunteer_for)
					assign_perm('edit', applicant.member, applicant.volunteer_for)
				else:
					remove_perm('add_page', applicant.member, applicant.volunteer_for)
					remove_perm('edit_page', applicant.member, applicant.volunteer_for)
					remove_perm('edit', applicant.member, applicant.volunteer_for)

			if "sec_moderator" in request.POST:
				if request.POST["sec_moderator"] == "true":
					assign_perm('moderate', applicant.member, applicant.volunteer_for)
				else:
					remove_perm('moderate', applicant.member, applicant.volunteer_for)

			if "status" in request.POST:
				applicant.status = request.POST["status"]
				for choice in applicant.STATUSCODES:
					if choice[0] == applicant.status:
						vals["statusdesc"] = choice[1]
			# And save!
			applicant.save()

		# Return a JSON-formated string to the client.
		vals["errors"] = errors
		return JsonResponse(vals)

