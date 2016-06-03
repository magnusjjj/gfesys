import requests
from django.shortcuts import redirect

from server.defaultview import DefaultView
from server.models import Server, rocketchat

# This is the motherload. The actual view that saves the server info.
class UpdateServerInfo(DefaultView):
	def post(self, request, server_id="0"):
		super(UpdateServerInfo, self).get(request)
		context = {}
		# Fetch (or create) the server
		if server_id == "0":
			context["server"] = Server()
		else:
			context["server"] = Server.objects.get(pk=server_id)

		try:
			# Fetch the access rights
			self.setrights_server(request, context, server_id)
		except:
			pass
		if request.user.is_administrator or context["volunteer"].sec_edit:
			# Modify the object
			context["server"].name = request.POST["name"]
			context["server"].description = request.POST["description"]
			context["server"].questions = request.POST["questions"]
			context["server"].status = request.POST["status"]
			rocketchannels = request.POST.getlist('rocketchannel')
			rocketchat.objects.filter(server=context["server"]).delete()
			for rocketchannel in rocketchannels:
				m = rocketchat()
				m.channelname = rocketchannel
				m.server = context["server"]
				if request.POST.get("rocketenabled", False) == "True":
					r = requests.post('http://chat.gfe.nu:1420/ChannelCreate', json={"ChannelName": rocketchannel, "ServerName": context["server"].name, "Enabled": "1"})
					m.rocketenabled = 1
				else:
					m.rocketenabled = 0
					r = requests.post('http://chat.gfe.nu:1420/ChannelCreate', json={"ChannelName": rocketchannel, "ServerName": context["server"].name, "Enabled": "0"})
				m.save()
			# Todo, handle errors here better:
			if 'image' in request.FILES:
				context["server"].image = request.FILES['image']

			# Save the object
			context["server"].save()

			return redirect("server:editserver", server_id=context["server"].id)

