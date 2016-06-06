from django.shortcuts import redirect

from server.defaultview import DefaultView
from server.models import Server


class UploadServerImage(DefaultView):
	def post(self, request, server_id):
		super(UploadServerImage, self).get(request)
		context = {}

		# Fetch the server
		context["server"] = Server.objects.get(pk=server_id)

		# Fetch our access rights
		self.setrights_server(request, context, server_id)

		# Security sanity check that we have edit rights
		if request.user.is_administrator or context["volunteer"].sec_edit:
			# Handle the image upload
			context["server"].image = request.FILES['image']
			context["server"].save()
			return redirect("editserver", server_id)