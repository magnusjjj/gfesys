# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.http import HttpResponse
from django.views.generic import View
from models import Server, Volunteer

# This file keeps some helper functions for the views in this app.

class DefaultView(View):
	context = {}
	def get(self, request):
		return
	
	# Gets the currently logged in user's access rights for the current user
	def setrights_server(self, request, server_id):
		# If we are logged in
		if 'member' in self.context:
			m = self.context["member"]
			s = Server.objects.get(pk=server_id)
			try:
				# And return if we find admin rights on the current user
				volun = Volunteer.objects.all().filter(member=m,server=s,status="OK")[0]
				self.context["volunteer"] = volun
			except:
				pass