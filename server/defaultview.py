from django.http import HttpResponse
from django.views.generic import View
from models import Server, Volunteer

class DefaultView(View):
	context = {}
	def get(self, request):
		return
	
	def setrights_server(self, request, server_id):
		if 'member' in self.context:
			m = self.context["member"]
			s = Server.objects.get(pk=server_id)
			try:
				volun = Volunteer.objects.all().filter(member=m,server=s,status="OK")[0]
				self.context["volunteer"] = volun
			except:
				pass