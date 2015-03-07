from django.shortcuts import render
from server.models import *
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

	
def login(request):
	return render(request, 'member/login.html')

@require_http_methods(["POST"])
def login_post(request):
	# Make a variable to hold all the errors in...
	errors = []
	context = {}
	login = request.POST["login"]
	password = request.POST["password"]
	try:
		themember = Member.objects.get(email__iexact=login)
	except:
		errors.append("Could not log in. Wrong username or password.")
		context["errors"] = errors
		return JsonResponse(context)
	
	if hashlib.sha512(password + themember.password_salt).hexdigest() == themember.password_hash:
		request.session['member_id'] = themember.id
	else:
		errors.append("Could not log in. Wrong username or password.")
	 
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
		themember = Member.objects.get(email__iexact=login)
	except:
		errors.append("Could not find a user with that email.")
		context["errors"] = errors
		return JsonResponse(context)
	
	salt = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(20))
	newpassword = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(10)) 
	newhash = hashlib.sha512(newpassword + salt).hexdigest()
	
	themember.password_salt = salt
	themember.password_hash = newhash
	themember.save()
	
	
	send_mail('Password reset', "Your new password is: \n\n" + newpassword, settings.EMAILFROM,
	[request.POST["login"].lower()], fail_silently=True)	

	context["errors"] = errors
	return JsonResponse(context)

def logout(request):
	del request.session['member_id']
	return JsonResponse({})

def register(request):
	values = {}
	context = {"countries": countries, "values": values}
	return render(request,'member/register.html', context)

@require_http_methods(["POST"])
def register_post(request):
	# Make a variable to hold all the errors in...
	errors = []
	context = {}
	
	#Make a list of all the fields we cant stand being empty.. :P
	notempty = {"country": "Country", "firstname": "First name", "surname": "Surname", "password": "Password",
	"adress": "Adress", "zip": "Zipcode", "birthdate": "Birthdate",
	"city": "City", "phone": "Phone", "login": "Email", "accept1": "Accept 1", "accept2": "Accept 2", "accept3": "Accept 3"}
	
	# Loop through them
	for field in notempty:
		if field not in request.POST or request.POST[field].strip() == "":
			# And begin setting errors
			errors.append("The field \"" + notempty[field] + "\" must not be empty")
	
	# Check the email adress...
	emailcheck = re.compile("^[^@]*@(.*)$")
	if "login" in request.POST and emailcheck.match(request.POST["login"]) is None:
		errors.append("Check the Email field, that does not look like an Email adress.")
	else:
		# Also check that its unique:
		doesnotexist = False
		try:
			Member.objects.get(email=request.POST["login"])
		except Member.DoesNotExist:
			doesnotexist = True
			
		if doesnotexist == False:
			errors.append("This Email is already taken. Contact support.")
	
	# Check the birthdate...
	datecheck = re.compile("^[0-9]{4}\\-[0-9]{2}\\-[0-9]{2}$")
	if "login" in request.POST and datecheck.match(request.POST["birthdate"]) is None:
		errors.append("Check the Birthdate field, the format should be YYYY-MM-DD.")
	
	# Check the password length...
	if "login" in request.POST and len(request.POST["password"]) < 8:
		errors.append("Your password needs to be at least 8 characters long.")
	
	# If its a swedish personnummer, check that its valid:
	
	if "socialsecuritynumber" in request.POST and "country" in request.POST:
		personnummer = request.POST["socialsecuritynumber"]
		personkoll = re.compile("^[0-9]{6}\\-[0-9]{4}$")
		if request.POST["country"] == "SE":
			if personkoll.match(personnummer) is not None:
				sum = 0
				n = 2
				
				personnummer = personnummer[:6] + personnummer[7:]
				for i in range(0,9):
					
					tmp = int(personnummer[i]) * n
					
					if (tmp > 9):
						sum += 1 + ((tmp % 10))
					else:
						sum += tmp
					if n == 2:
						n = 1
					else:
						n = 2
				if ((sum + int(personnummer[9])) % 10) != 0:
					errors.append("Your Swedish social security number is incorrect. Please double check.")
				else:
					pass
			else:
				errors.append("Your Swedish social security number is specified in the wrong format. The correct format is YYMMDD-XXXX")
		# Also check that its unique:
		doesnotexist = False
		try:
			Member.objects.get(socialsecuritynumber=request.POST["socialsecuritynumber"])
		except Member.DoesNotExist:
			doesnotexist = True
			
		if doesnotexist == False:
			errors.append("This SSID is already taken. Contact support.")
	
	# Now, we need to make a member
	
	if len(errors) == 0:
		salt = ''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(20)) 
		
		member = Member.objects.create(
			firstname= request.POST["firstname"],
			surname= request.POST["surname"],
			nick= "",
			birthdate= request.POST["birthdate"],
			phone= request.POST["phone"],
			mobile= request.POST["other_phone"],
			street= request.POST["adress"],
			city= request.POST["city"],
			country_id= request.POST["country"],
			zip= request.POST["zip"],
			careof= request.POST["careof"],
			socialsecuritynumber= request.POST["socialsecuritynumber"],
			email= request.POST["login"].lower(),
			refreshedon= datetime.datetime.now(),
			password_hash= hashlib.sha512(request.POST["password"] + salt).hexdigest(),
			password_salt= salt,
			image_height=0,
			image_width=0,
		)
		
		member.save()
		request.session['member_id'] = member.id
		
		send_mail('Welcome to GFE!', "Welcome to GFE!\n\n Your username is: \n\n" + request.POST["login"].lower() + "\n\n , and your password is known only to you.\n\n", settings.EMAILFROM,
		[request.POST["login"].lower()], fail_silently=True)
		
	context["errors"] = errors
	return JsonResponse(context) 