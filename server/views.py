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
from page import views
from page.models import *
from django.contrib.contenttypes.models import ContentType
from newsletter.models import *

# This file is a bit messy, i must admit.
# It holds all of the Views, the code that is called when a page is requested.
# It should be split up a bit more (see the membership code)
# Alas, I could not get my thumb out of my anus.

class StripSettings:
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
		'span',
		'div',
		'img',
		'h1',
		'h2',
		'h3',
		'h4',
		'h5'
	]

	# Like the above, but 'safe' attributes
	ALLOWED_ATTRIBUTES = {
		'a': ['href', 'title'],
		'abbr': ['title'],
		'acronym': ['title'],
		'img': ['src'],
		'*': ['class']
	}
	
	# Like the above, but safe styles. Mmmmmyup.
	
	ALLOWED_STYLES = []


# This view is for the listing of all the servers
class ViewIndex(DefaultView):
	def get(self, request):
		super(ViewIndex, self).get(request)
		context = {}
		status_list = [Server.STATUS_LIVE, Server.STATUS_TESTING]
		if hasattr(request.user, 'is_administrator') and request.user.is_administrator:
			status_list.append(Server.STATUS_DRAFT)
		# Get all the servers, and order by id.
		context["servers"] = Server.objects.filter(status__in=status_list).order_by('status','id')
		
		context["news"] = Submission.objects.filter(publish=True)
		
		# Render that thing right up
		return render(request,'servers/index.html', context)

class ViewServerList(DefaultView):
	def get(self, request):
		super(ViewIndex, self).get(request)
		context = {}
		status_list = [Server.STATUS_LIVE, Server.STATUS_TESTING]
		if hasattr(request.user, 'is_administrator') and request.user.is_administrator:
			status_list.append(Server.STATUS_DRAFT)
		# Get all the servers, and order by id.
		context["servers"] = Server.objects.filter(status__in=status_list).order_by('status','id')
		# Render that thing right up
		return render(request,'servers/index.html', context)

# This view is for viewing a specific server
class ViewDetail(DefaultView):	
	def get(self, request, slug, slug_page=None):
		super(ViewDetail, self).get(request)
		context = {}
		# Get the server in question
		context["server"] = Server.objects.get(slug=slug)
		
		# Find out if we have editing rights to said server
		self.setrights_server(request, context, context["server"].pk)
		context["request"] = request
		
		# Get a list of text pages for this server
		context["pages"] = Page.objects.filter(parent_object_id=context["server"].pk,
									parent_content_type=ContentType.objects.get_for_model(context["server"]))
		# What page is active?
		if slug_page is None:
			try:
				context["page_active"] = context["pages"][0].slug
			except:
				context["page_active"] = ""
		else:
			context["page_active"] = slug_page
		
		# Get a list of volunteers for the server
		context["volunteers"] = Volunteer.objects.all().filter(server=context["server"],status="OK")
		# And, BAM, render that thing.
		return render(request,'servers/detail.html', context)

# This view is for an admin, allowing them to manage the list of volunteers
class ViewManageVolunteers(DefaultView):
	def get(self, request, server_id):
		super(ViewManageVolunteers, self).get(request)
		context = {}
		# Get the server in question
		context["server"] = Server.objects.get(pk=server_id)
		# Find out if we have editing rights to said server
		self.setrights_server(request, context, server_id)
		# Get the list of volunteers...
		context["applicants"] = Volunteer.objects.filter(server=context["server"])
		# Now render it. So hard.
		return render(request,'servers/managevolunteers.html', context)

# This view is used when a user wants to send in an application to become a volunteer
class ViewVolunteerFor(DefaultView):
	def get(self, request, server_id):
		super(ViewVolunteerFor, self).get(request)
		context = {}
		# Get the server in question
		context["server"] = Server.objects.get(pk=server_id)
		# Render it
		return render(request,'servers/volunteer.html', context)
	
	def post(self, request, server_id):
		super(ViewVolunteerFor, self).get(request)
		context = {}
		# Get the server in question
		context["server"] = Server.objects.get(pk=server_id)
		# Display a shiny message
		context["hasposted"] = True
		
		# Create and save a volunteer
		vol = Volunteer.objects.create(
			member = request.user,
			server = context["server"],
			answer = request.POST["answer"],
			role = "",
		)
		
		vol.save()
		
		# Render. Wooooo.
		return render(request,'servers/volunteer.html', context)


# This is a view to save changes to a volunteer, for the server admins to use. AJAX, responds with a JSON string.
class ServerEditApplicant(DefaultView):
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
		if not request.user.is_administrator:
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

# Like the above, but simply returns the answers that the volunteer filled in while applying
class ServerViewAnswers(DefaultView):
	def post(self, request):
		super(ServerViewAnswers, self).get(request)
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

		# And render
		if request.user.is_administrator or context["volunteer"].sec_edit:
			return render(request,'servers/editserver.html', context)
	
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
			
			# Todo, handle errors here better: 
			if 'image' in request.FILES:
				context["server"].image = request.FILES['image']
			
			# Save the object
			context["server"].save()
			
			return redirect("server:editserver", server_id=context["server"].id)

# Like the name applies, handles image uploads for servers
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

class AddPage(DefaultView):
	def get(self, request, server_id):
		super(AddPage, self).get(request)
		context = {}
		# Fetch the server
		context["server"] = Server.objects.get(pk=server_id)
		
		# Empty page, for the view
		page = Page()
		context["page"] = page
		
		# Fetch our access rights
		self.setrights_server(request, context, server_id)
		
		# Security sanity check that we have edit rights
		if request.user.is_administrator or context["volunteer"].sec_edit:
			# Some sort of wierd error causes the request to point to the wrong place. What?
			context["request"] = request
			return render(request,'servers/addpage.html', context)
	
	def post(self, request, server_id):
		super(AddPage, self).get(request)
		server = Server.objects.get(pk=server_id)
		context = {}
		# Fetch the server
		context["server"] = Server.objects.get(pk=server_id)
		
		# Fetch our access rights
		self.setrights_server(request, context, server_id)
		
		# Security sanity check that we have edit rights
		if request.user.is_administrator or context["volunteer"].sec_edit:
			# Some sort of wierd error causes the request to point to the wrong place. What?
			context["request"] = request
			strip = StripSettings()
			page = views.handle_save(request, None, server, strip)
			return redirect(server)

class DeletePage(DefaultView):
	def get(self, request, page_id):
		super(DeletePage, self).get(request)
		context = {}
		# Fetch Page
		page = Page.objects.get(pk=page_id)
		
		if type(page.parent) is Server:
			# Fetch the server
			context["server"] = page.parent
			
			# Fetch our access rights
			self.setrights_server(request, context, page.parent.pk)
		
			# Security sanity check that we have edit rights
			if request.user.is_administrator or context["volunteer"].sec_edit:
				page.delete()
				return redirect(page.parent)
	
class EditPage(DefaultView):
	def get(self, request, page_id):
		super(EditPage, self).get(request)
		context = {}
		# Fetch Page
		page = Page.objects.get(pk=page_id)
		context["page"] = page
		
		if type(page.parent) is Server:
			# Fetch the server
			context["server"] = page.parent
			
			# Fetch our access rights
			self.setrights_server(request, context, page.parent.pk)
			
			# Security sanity check that we have edit rights
			if request.user.is_administrator or context["volunteer"].sec_edit:
				return render(request,'servers/addpage.html', context)
	
	def post(self, request, page_id):
		super(EditPage, self).get(request)
		context = {}
		# Fetch Page
		page = Page.objects.get(pk=page_id)
		context["page"] = page
		
		if type(page.parent) is Server:
			# Fetch the server
			context["server"] = page.parent
			
			# Fetch our access rights
			self.setrights_server(request, context, page.parent.pk)
			strip = StripSettings()
			
			# Security sanity check that we have edit rights
			if request.user.is_administrator or context["volunteer"].sec_edit:
				page = views.handle_save(request, page_id, context["server"], strip)
				return redirect(context["server"])
	
class SubmissionArchiveDetailOverrideView(DefaultView):
	def get(self, request, newsletter_slug, year, month, day, slug):
		themessage = Message.objects.get(slug=slug)
		return render(request,'newsletter/message/message_online.html', {"message": themessage, "newsletter": themessage.newsletter})