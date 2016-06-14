from django.http import JsonResponse

from server.profileapi.models import Volunteer
from django.views.generic import View

# This is a view to save changes to a volunteer, for the server admins to use. AJAX, responds with a JSON string.
class ServerEditApplicant(View):
	def post(self, request):
		super(ServerEditApplicant, self).get(request)
		context = {}
		# Fetch the volunteer
		applicant = Volunteer.objects.get(pk=int(request.POST["applicant_id"]))

		# Fetch our access rights
		self.setrights_server(request, context, applicant.server_id)

		# A simple list to hold error messages in
		errors = []

		# And a dictionary to hold stuff to put in the JSON-response in
		vals = {}

		# Sanity check that we have editing rights
		if not request.user.is_administrator:# This view is used when a user wants to send in an application to become a volunteer
			if context["volunteer"].sec_accept:
				errors.push("You don't have access to this command")
		else:
			# Edit the values requested:
			if "role" in request.POST:
				applicant.role = request.POST["role"]

			if "sec_accept" in request.POST:
				if request.POST["sec_accept"] == "true":
					applicant.sec_accept = True
				else:
					applicant.sec_accept = False

			if "sec_edit" in request.POST:
				if request.POST["sec_edit"] == "true":
					applicant.sec_edit = True
				else:
					applicant.sec_edit = False

			if "sec_moderator" in request.POST:
				if request.POST["sec_moderator"] == "true":
					applicant.sec_moderator = True
				else:
					applicant.sec_moderator = False

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

