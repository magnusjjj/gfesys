from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from server.models import *
from server.defaultview import DefaultView
from django.http import JsonResponse
import bleach
# Create your views here.

class ViewIndex(DefaultView):
	def get(self, request):
		super(ViewIndex, self).get(request)
		self.context["servers"] = Server.objects.order_by('id')
		return render(request,'servers/index.html', self.context)

class ViewDetail(DefaultView):	
	def get(self, request, server_id):
		super(ViewDetail, self).get(request)
		self.setrights_server(request, server_id)
		self.context["server"] = Server.objects.get(pk=server_id)
		self.context["volunteers"] = Volunteer.objects.all().filter(server=self.context["server"],status="OK")
		return render(request,'servers/detail.html', self.context)
		
class ViewManageVolunteers(DefaultView):
	def get(self, request, server_id):
		super(ViewManageVolunteers, self).get(request)
		self.context["server"] = Server.objects.get(pk=server_id)
		self.setrights_server(request, server_id)
		self.context["applicants"] = Volunteer.objects.all().filter(server=self.context["server"])
		return render(request,'servers/managevolunteers.html', self.context)

class ViewVolunteerFor(DefaultView):
	def get(self, request, server_id):
		super(ViewVolunteerFor, self).get(request)
		self.context["server"] = Server.objects.get(pk=server_id)
		return render(request,'servers/volunteer.html', self.context)
	
	def post(self, request, server_id):
		super(ViewVolunteerFor, self).get(request)
		self.context["server"] = Server.objects.get(pk=server_id)
		self.context["hasposted"] = True
		vol = Volunteer.objects.create(
			member = self.context["member"],
			server = self.context["server"],
			answer = request.POST["answer"],
			role = "",
		)
		vol.save()
		return render(request,'servers/volunteer.html', self.context)

class ServerEditApplicant(DefaultView):
	def post(self, request):
		super(ServerEditApplicant, self).get(request)
		applicant = Volunteer.objects.get(pk=int(request.POST["applicant_id"]))
		self.setrights_server(request, applicant.server_id)
		errors = []
		
		vals = {}
		
		if not self.context["volunteer"].sec_accept:
			errors.push("You don't have access to this command")
		else:
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
			
			if "status" in request.POST:
				applicant.status = request.POST["status"]
				for choice in applicant.STATUSCODES:
					if choice[0] == applicant.status:
						vals["statusdesc"] = choice[1]
			applicant.save()
		vals["errors"] = errors
		return JsonResponse(vals)

class ServerViewAnswers(DefaultView):
	def post(self, request):
		super(ServerViewAnswers, self).get(request)
		applicant = Volunteer.objects.get(pk=int(request.POST["applicant_id"]))
		self.setrights_server(request, applicant.server_id)
		errors = []
		
		vals = {}
		
		if not self.context["volunteer"].sec_accept:
			errors.push("You don't have access to this command")
		else:
			vals["content"] = applicant.answer
			vals["title"] = applicant.member.firstname + ' ' + applicant.member.surname + "'s answers"
		vals["errors"] = errors
		return JsonResponse(vals)

class EditServer(DefaultView):
	def get(self, request, server_id):
		super(EditServer, self).get(request)
		self.context["server"] = Server.objects.get(pk=server_id)
		self.setrights_server(request, server_id)
		if self.context["volunteer"].sec_edit:
			return render(request,'servers/editserver.html', self.context)
		
class UpdateServerInfo(DefaultView):
	ALLOWED_TAGS = [
		'a',
		'abbr',
		'acronym',
		'b',
		'blockquote',
		'code',
		'em',
		'i',
		'li',
		'ol',
		'strong',
		'ul',
		'p',
	]

	ALLOWED_ATTRIBUTES = {
		'a': ['href', 'title'],
		'abbr': ['title'],
		'acronym': ['title'],
	}
	
	ALLOWED_STYLES = []

	def post(self, request, server_id):
		super(UpdateServerInfo, self).get(request)
		self.context["server"] = Server.objects.get(pk=server_id)
		self.setrights_server(request, server_id)
		if self.context["volunteer"].sec_edit:
			self.context["server"].name = request.POST["name"]
			self.context["server"].description = request.POST["description"]
			self.context["server"].howto = bleach.clean(request.POST["howto"], self.ALLOWED_TAGS, self.ALLOWED_ATTRIBUTES, self.ALLOWED_STYLES)
			self.context["server"].rules = bleach.clean(request.POST["rules"], self.ALLOWED_TAGS, self.ALLOWED_ATTRIBUTES, self.ALLOWED_STYLES)
			self.context["server"].questions = request.POST["questions"]
			self.context["server"].save()
			return redirect("editserver", server_id)
		
class UploadServerImage(DefaultView):
	def post(self, request, server_id):
		super(UploadServerImage, self).get(request)
		self.context["server"] = Server.objects.get(pk=server_id)
		self.setrights_server(request, server_id)
		if self.context["volunteer"].sec_edit:
			self.context["server"].image = request.FILES['image']
			self.context["server"].save()
			return redirect("editserver", server_id)