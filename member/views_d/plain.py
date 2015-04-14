# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.shortcuts import render
from server.models import *
from django_countries import countries

# Both of these Views are *tiny*, and just renders html for two popups.

def login(request):
	return render(request, 'member/login.html')

def register(request):
	values = {}
	context = {"countries": countries, "values": values}
	return render(request,'member/register.html', context)