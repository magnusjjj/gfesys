# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.shortcuts import render
from server.models import *
from member.models import Member
from django_countries import countries
from django.http import JsonResponse
import datetime
import re
import random
import string
import hashlib
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from oauth2_provider.views.generic import ProtectedResourceView
import django.contrib.auth
from django.db.models import Q
import json

@require_http_methods(["POST"])
def login_post(request):
	# Make a variable to hold all the errors in...
	errors = []
	context = {}
	login_name = request.POST["login"]
	password = request.POST["password"]
	
	user = authenticate(username=login_name, password=password)
	if user is None:
		errors.append("Could not log in. Wrong username or password.")
		context["errors"] = errors
		return JsonResponse(context)
	else:
		if user.is_active:
			login(request, user)
			try: 
				context["redirectto"] = request.POST["next"]
			except:
				pass
		else:
			errors.append("Your account is for some reason set as not being logged-in-able. Contact support.")
	context["errors"] = errors
	
	return JsonResponse(context)

@require_http_methods(["POST"])
def forgot_post(request):
	# Make a variable to hold all the errors in...
	errors = []
	context = {}
	login = request.POST["login"]
	themember = {}
	try:
		themember = Member.objects.get(Q(username__iexact=login) | Q(email__iexact=login))
	except:
		errors.append("Could not find a user with that email or username.")
		context["errors"] = errors
		return JsonResponse(context)
	
	newpassword = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(10)) 
	
	themember.set_password(newpassword)
	themember.save()
	
	
	send_mail('Password reset', "Your new password is: \n\n" + newpassword, settings.EMAILFROM,
	[themember.email], fail_silently=True)	

	context["errors"] = errors
	return JsonResponse(context)
	
@require_http_methods(["POST"])
def register_post(request):
	# Make a variable to hold all the errors in...
	errors = []
	context = {}
	
	#Make a list of all the fields we cant stand being empty.. :P
	notempty = {"password": "Password","email": "Email", "accept": "Accept", "username": "Username"}
	
	# Loop through them
	for field in notempty:
		if field not in request.POST or request.POST[field].strip() == "":
			# And begin setting errors
			errors.append("The field \"" + notempty[field] + "\" must not be empty")
	
	# Check the email adress...
	emailcheck = re.compile("^[^@]*@(.*)$")
	if "email" in request.POST and emailcheck.match(request.POST["email"]) is None:
		errors.append("Check the Email field, that does not look like an Email adress.")
	else:
		# Also check that its unique:
		doesnotexist = False
		try:
			Member.objects.get(email=request.POST["email"])
		except Member.DoesNotExist:
			doesnotexist = True
			
		if doesnotexist == False:
			errors.append("This Email is already taken. Contact support.")
	
	# Check that the username does not already exist adress...
	if "username" in request.POST:
		try:
			member = Member.objects.get(username=request.POST["username"]) # This will trigger an exception if not found
			errors.append("That user already exists!" + member)
		except:
			pass
	
	# Check the password length...
	if "email" in request.POST and len(request.POST["password"]) < 8:
		errors.append("Your password needs to be at least 8 characters long.")
	
	# Now, we need to make a user
	
	if len(errors) == 0:
		salt = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(20)) 
		
		member = Member.objects.create(
			first_name= "",
			last_name= "",
			nick= "",
			birthdate= "",
			phone= "",
			mobile= "",
			street= "",
			city= "",
			country_id= "",
			zip= "",
			careof= "",
			socialsecuritynumber= "",
			email= request.POST["email"].lower(),
			username= request.POST["username"].lower(),
			refreshedon= datetime.datetime.now(),
			image_height=0,
			image_width=0,
			is_active=1,
			membership_populated=False,
		)
		
		member.save()
		member.set_password(request.POST["password"])
		member.save()
		
		
		user = authenticate(username=member.username, password=request.POST["password"])
		if user is None:
			errors.append("Could not log in. Thats really wierd.")
			context["errors"] = errors
			return JsonResponse(context)
		else:
			if user.is_active:
				login(request, user)
				try: 
					context["redirectto"] = request.POST["next"]
				except:
					pass
			else:
				errors.append("Your account is for some reason set as not being logged-in-able. Contact support. This is super duper wierd.")
		send_mail('Welcome to GFE!', "Welcome to GFE!\n\n Your username is: \n\n" + request.POST["username"].lower() + "\n\n , and your password is known only to you.\n\n", settings.EMAILFROM,
		[request.POST["email"].lower()], fail_silently=True)		
	context["errors"] = errors
	return JsonResponse(context)
	
def logout(request):
	django.contrib.auth.logout(request)
	return JsonResponse({})

@login_required()
def me(request):
	return JsonResponse({"id": request.user.id, "name": request.user.first_name + ' ' + request.user.last_name, 'username': request.user.username, 'email': request.user.email})
