# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.shortcuts import render
from server.models import *
from django_countries import countries
from member.models import Member
import re
from django_countries import countries
import datetime

def members_index(request):
	context = {}
	context["members"] = Member.objects.filter(is_opt_in=True)
	return render(request,'member/members_index.html', context)
	
def members_view(request, member_id):
	context = {}
	context["member"] = Member.objects.get(pk=member_id)
	return render(request,'member/members_view.html', context)

def become_member(request):
	context = {}
	# Make a variable to hold all the errors in...
	errors = []

	currmember = request.user


	context["member"] = currmember
	context["countries"] = countries

	if request.method == 'GET':
		return render(request,'member/become_member.html', context)
	elif request.method == 'POST':
		#Make a list of all the fields we cant stand being empty.. :P
		notempty = {"country": "Country", "first_name": "First name", "last_name": "Surname",
		"adress": "Adress", "zip": "Zipcode", "birthdate": "Birthdate",
		"city": "City", "phone": "Phone", "accept1": "Accept 1", "accept2": "Accept 2", "accept3": "Accept 3"}
	
		# Loop through them
		for field in notempty:
			if field not in request.POST or request.POST[field].strip() == "":
				# And begin setting errors
				errors.append("The field \"" + notempty[field] + "\" must not be empty")
	
	
		# Check the birthdate...
		datecheck = re.compile("^[0-9]{4}\\-[0-9]{2}\\-[0-9]{2}$")
		if datecheck.match(request.POST["birthdate"]) is None:
			errors.append("Check the Birthdate field, the format should be YYYY-MM-DD.")
	
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
					testmember = Member.objects.get(socialsecuritynumber=request.POST["socialsecuritynumber"])
					if testmember.pk == currmember.pk:
						doesnotexist = True
				except:
					doesnotexist = True
				
				if doesnotexist == False:
					errors.append("This SSID is already taken. Contact support.")
	
		# Temporarily change the member in memory, so that postback works when erroring
		currmember.first_name= request.POST["first_name"]
		currmember.last_name= request.POST["last_name"]
		currmember.nick= ""
		currmember.birthdate= request.POST["birthdate"]
		currmember.phone= request.POST["phone"]
		currmember.mobile= request.POST["other_phone"]
		currmember.street= request.POST["adress"]
		currmember.city= request.POST["city"]
		currmember.country_id= request.POST["country"]
		currmember.zip= request.POST["zip"]
		currmember.careof= request.POST["careof"]
		currmember.socialsecuritynumber= request.POST["socialsecuritynumber"]
		currmember.refreshedon= datetime.datetime.now()
		currmember.membership_populated = True
		
		# If there are no errors, save the member		
		if len(errors) == 0:
			currmember.save()
		
		context["errors"] = errors
		context["member"] = currmember
		return render(request,'member/become_member.html', context)
