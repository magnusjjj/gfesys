from django.http import JsonResponse

from profileapi.models import Volunteer
from django.views.generic import View
from profileapi.helpers.ProfileView import ProfileView

# Like the above, but simply returns the answers that the volunteer filled in while applying
class ViewAnswers(ProfileView):
	def post(self, request):
		super(ViewAnswers, self).get(request)
		# Get the applicant
		applicant = Volunteer.objects.get(pk=int(request.POST["applicant_id"]))

		# Fetch our access rights
		self.setrights_server(request, context, applicant.server_id)

		# A simple list for the errors, and a dictionary for the return values
		errors = []
		vals = {}

		# Sanity check that we have edit rights
		if not context["volunteer"].sec_accept:
			errors.push("You don't have access to this command")
		else:
			# Just format the response a little bit
			vals["content"] = applicant.answer
			vals["title"] = applicant.member.firstname + ' ' + applicant.member.surname + "'s answers"

		# And return a JSON response
		vals["errors"] = errors
		return JsonResponse(vals)

