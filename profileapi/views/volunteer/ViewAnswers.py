from django.http import JsonResponse

from profileapi.models import Volunteer
from django.views.generic import View
from profileapi.helpers.ProfileView import ProfileView

# Simply returns the answers that the volunteer filled in while applying
class ViewAnswers(ProfileView):
	def post(self, request):
		# Get the applicant
		applicant = Volunteer.objects.get(pk=int(request.POST["applicant_id"]))

		# A simple list for the errors, and a dictionary for the return values
		errors = []
		vals = {}

		# Sanity check that we have edit rights
		if not request.user.has_perm("volunteer_edit", applicant.volunteer_for):
			errors.push("You don't have access to this command")
		else:
			# Just format the response a little bit
			vals["content"] = applicant.answer
			vals["title"] = applicant.member.firstname + ' ' + applicant.member.surname + "'s answers"

		# And return a JSON response
		vals["errors"] = errors
		return JsonResponse(vals)

