# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.shortcuts import render
from server.models import *
from django_countries import countries
from member.models import Member

def members_index(request):
	context = {}
	context["members"] = Member.objects.filter(is_opt_in=True)
	return render(request,'member/members_index.html', context)
	
def members_view(request, member_id):
	context = {}
	context["member"] = Member.objects.get(pk=member_id)
	return render(request,'member/members_view.html', context)

def become_member(request):
	# Make a variable to hold all the errors in...
	errors = []
	context = {}
	
	#Make a list of all the fields we cant stand being empty.. :P
	notempty = {"country": "Country", "first_name": "First name", "last_name": "Surname", "password": "Password",
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
			first_name= request.POST["first_name"],
			last_name= request.POST["last_name"],
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
			username= request.POST["login"].lower(),
			refreshedon= datetime.datetime.now(),
			image_height=0,
			image_width=0,
			is_active=1,
		)
		
		member.save()
		member.set_password(request.POST["password"])
		member.save()
		
		
		user = authenticate(username=member.username, password=request.POST["password"])
		
		send_mail('Welcome to GFE!', "Welcome to GFE!\n\n Your username is: \n\n" + request.POST["login"].lower() + "\n\n , and your password is known only to you.\n\n", settings.EMAILFROM,
		[request.POST["login"].lower()], fail_silently=True)
		
	context["errors"] = errors
	return JsonResponse(context)
