from django.template import loader, RequestContext
from models import Member, Server, Volunteer
from django.core.urlresolvers import resolve
from django.core.cache import cache

def context(request):
	cache.clear()
	context = {}
	
	app_name = resolve(request.path).app_name
	
	if app_name == "server":
		context["section"] = "servers"
	if app_name == "member":
		context["section"] = "members"
	if app_name == "spirit":
		context["section"] = "forums"
	
	context["app_name"] = app_name
	
	return context