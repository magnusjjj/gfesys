# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

# This file handles what url's are mapped to what view.
# This is much better explained in the Django manual,
# and we don't do anything freakier than what is explained in the tutorials. Promise <3
# https://docs.djangoproject.com/en/1.8/topics/http/urls/

from django.conf.urls import url, include
from server.views_normal.ViewIndex import ViewIndex
from profileapi.views.profile.ViewProfileList import ViewProfileList

from models import Server

urlpatterns = [
					url(r'^$', ViewIndex.as_view(profilemodel=Server), name='index'),
					url(r'^$servers/', ViewProfileList.as_view(profilemodel=Server), name='serverlist'),
					url('', include("server.profileurls", namespace="server_profile")),
				]
