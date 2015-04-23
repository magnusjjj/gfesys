# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from server.models import *
from server.defaultview import DefaultView
from django.http import JsonResponse
import bleach

# This file is a bit messy, i must admit.
# It holds all of the Views, the code that is called when a page is requested.
# It should be split up a bit more (see the membership code)
# Alas, I could not get my thumb out of my anus.


# This view is for the listing of all the servers
class ViewIndex(DefaultView):
	def get(self, request):
		super(ViewIndex, self).get(request)
		# Get all the servers, and order by id.
		self.context["servers"] = Server.objects.order_by('id')
		# Render that thing right up
		return render(request,'servers/index.html', self.context)

# This view is for viewing a specific server
class ViewDetail(DefaultView):	
	def get(self, request, server_id):
		super(ViewDetail, self).get(request)
		# Find out if we have editing rights to said server
		self.setrights_server(request, server_id)
		# And get the server in question
		self.context["server"] = Server.objects.get(pk=server_id)
		self.context["request"] = request
		# Get a list of volunteers for the server
		self.context["volunteers"] = Volunteer.objects.all().filter(server=self.context["server"],status="OK")
		# And, BAM, render that thing.
		return render(request,'servers/detail.html', self.context)

# This view is for an admin, allowing them to manage the list of volunteers
class ViewManageVolunteers(DefaultView):
	def get(self, request, server_id):
		super(ViewManageVolunteers, self).get(request)
		# Get the server in question
		self.context["server"] = Server.objects.get(pk=server_id)
		# Find out if we have editing rights to said server
		self.setrights_server(request, server_id)
		# Get the list of volunteers...
		self.context["applicants"] = Volunteer.objects.all().filter(server=self.context["server"])
		# Now render it. So hard.
		return render(request,'servers/managevolunteers.html', self.context)

# This view is used when a user wants to send in an application to become a volunteer
class ViewVolunteerFor(DefaultView):
	def get(self, request, server_id):
		super(ViewVolunteerFor, self).get(request)
		# Get the server in question
		self.context["server"] = Server.objects.get(pk=server_id)
		# Render it
		return render(request,'servers/volunteer.html', self.context)
	
	def post(self, request, server_id):
		super(ViewVolunteerFor, self).get(request)
		# Get the server in question
		self.context["server"] = Server.objects.get(pk=server_id)
		# Display a shiny message
		self.context["hasposted"] = True
		
		# Create and save a volunteer
		vol = Volunteer.objects.create(
			member = request.user,
			server = self.context["server"],
			answer = request.POST["answer"],
			role = "",
		)
		
		vol.save()
		
		# Render. Wooooo.
		return render(request,'servers/volunteer.html', self.context)


# This is a view to save changes to a volunteer, for the server admins to use. AJAX, responds with a JSON string.
class ServerEditApplicant(DefaultView):
	def post(self, request):
		super(ServerEditApplicant, self).get(request)
		# Fetch the volunteer
		applicant = Volunteer.objects.get(pk=int(request.POST["applicant_id"]))
		
		# Fetch our access rights
		self.setrights_server(request, applicant.server_id)
		
		# A simple list to hold error messages in
		errors = []
		
		# And a dictionary to hold stuff to put in the JSON-response in
		vals = {}
		
		# Sanity check that we have editing rights
		if not request.user.is_administrator:
			if self.context["volunteer"].sec_accept:
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

# Like the above, but simply returns the answers that the volunteer filled in while applying
class ServerViewAnswers(DefaultView):
	def post(self, request):
		super(ServerViewAnswers, self).get(request)
		# Get the applicant
		applicant = Volunteer.objects.get(pk=int(request.POST["applicant_id"]))
		
		# Fetch our access rights
		self.setrights_server(request, applicant.server_id)
		
		# A simple list for the errors, and a dictionary for the return values
		errors = []
		vals = {}
		
		# Sanity check that we have edit rights
		if not self.context["volunteer"].sec_accept:
			errors.push("You don't have access to this command")
		else:
			# Just format the response a little bit
			vals["content"] = applicant.answer
			vals["title"] = applicant.member.firstname + ' ' + applicant.member.surname + "'s answers"
		
		# And return a JSON response
		vals["errors"] = errors
		return JsonResponse(vals)

# Simply the view that *renders* the edit screen
class EditServer(DefaultView):
	def get(self, request, server_id=0):
		super(EditServer, self).get(request)
		
		# Fetch (or create) the server
		if server_id == 0:
			self.context["server"] = Server()
		else:
			self.context["server"] = Server.objects.get(pk=server_id)
		
		# Load the access rights
		self.setrights_server(request, server_id)
		
		self.context["server_id"] = server_id
		
		# And render
		if request.user.is_administrator or self.context["volunteer"].sec_edit:
			return render(request,'servers/editserver.html', self.context)
	
# This is the motherload. The actual view that saves the server info.	
class UpdateServerInfo(DefaultView):
	# Simple list with a bunch of.. 'safe' html tags
	
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

	# Like the above, but 'safe' attributes
	
	ALLOWED_ATTRIBUTES = {
		'a': ['href', 'title'],
		'abbr': ['title'],
		'acronym': ['title'],
	}
	
	# Like the above, but safe styles. Mmmmmyup.
	
	ALLOWED_STYLES = []

	def post(self, request, server_id="0"):
		super(UpdateServerInfo, self).get(request)
		# Fetch (or create) the server
		if server_id == "0":
			self.context["server"] = Server()
		else:
			self.context["server"] = Server.objects.get(pk=server_id)
		
		# Fetch the access rights
		self.setrights_server(request, server_id)
		
		if request.user.is_administrator or self.context["volunteer"].sec_edit:
			# Modify the object
			self.context["server"].name = request.POST["name"]
			self.context["server"].description = request.POST["description"]
			
			# Bleach is the tool for safe-i-fying html code
			self.context["server"].howto = bleach.clean(request.POST["howto"], self.ALLOWED_TAGS, self.ALLOWED_ATTRIBUTES, self.ALLOWED_STYLES)
			self.context["server"].rules = bleach.clean(request.POST["rules"], self.ALLOWED_TAGS, self.ALLOWED_ATTRIBUTES, self.ALLOWED_STYLES)
			self.context["server"].questions = request.POST["questions"]
			
			# Todo, handle errors here better: 
			if 'image' in request.FILES:
				self.context["server"].image = request.FILES['image']
			
			# Save the object
			self.context["server"].save()
			
			return redirect("server:editserver", server_id=self.context["server"].id)

# Like the name applies, handles image uploads for servers
class UploadServerImage(DefaultView):
	def post(self, request, server_id):
		super(UploadServerImage, self).get(request)
		
		# Fetch the server
		self.context["server"] = Server.objects.get(pk=server_id)
		
		# Fetch our access rights
		self.setrights_server(request, server_id)
		
		# Security sanity check that we have edit rights
		if self.context["volunteer"].sec_edit:
			# Handle the image upload
			self.context["server"].image = request.FILES['image']
			self.context["server"].save()
			return redirect("editserver", server_id)