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