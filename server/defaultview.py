from django.http import HttpResponse
from django.views.generic import View
from models import Member, Server, Volunteer

class DefaultView(View):
	context = {}
	def get(self, request):
		if "member_id" in request.session:
			self.context["member"] = Member.objects.get(pk=request.session["member_id"])
	
	def setrights_server(self, request, server_id):
		m = self.context["member"]
		s = Server.objects.get(pk=server_id)
		try:
			volun = Volunteer.objects.all().filter(member=m,server=s,status="OK")[0]
			self.context["volunteer"] = volun
		except:
			pass