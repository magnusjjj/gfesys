from django.shortcuts import render

from server.defaultview import DefaultView
from server.models import Server, rocketchat

# Simply the view that *renders* the edit screen
class EditServer(DefaultView):
	def get(self, request, server_id=0):
		context = {}
		super(EditServer, self).get(request)

		# Fetch (or create) the server
		if server_id == 0:
			context["server"] = Server()
			if not (request.user.is_administrator):
				raise ValueError('You dont have access to this function. Boo!')
		else:
			context["server"] = Server.objects.get(pk=server_id)
			# Load the access rights
			self.setrights_server(request, context, server_id)
			if not (request.user.is_administrator or context["volunteer"].sec_edit):
				raise ValueError('You dont have access to this function. Boo!')
		context["server_id"] = server_id
		context["server"] = Server.objects.get(pk=server_id)
		context["channels"] = rocketchat.objects.filter(server=context["server"])
		# And render
		if request.user.is_administrator or context["volunteer"].sec_edit:
			return render(request,'servers/editserver.html', context)

