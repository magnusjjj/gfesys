# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.core.urlresolvers import resolve


# This file is kindof a proxy deal, that sets some variables
# we need all over the system, like the current user, 
# or which menu item is selected

def context(request):
	context = {}
	
	res = resolve(request.path)
	
	# Check which menu item to show as selected
	app_name = res.app_name
	
	if app_name == "server":
		context["section"] = "servers"
	if app_name == "member":
		context["section"] = "members"
	if app_name == "spirit":
		context["section"] = "forums"
	if app_name == "page":
		context["section"] = "page"
		
	context["app_name"] = app_name
	
	return context
