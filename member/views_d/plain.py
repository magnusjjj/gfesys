from django.shortcuts import render
from server.models import *
from django_countries import countries

def login(request):
	return render(request, 'member/login.html')

def register(request):
	values = {}
	context = {"countries": countries, "values": values}
	return render(request,'member/register.html', context)