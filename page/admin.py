# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.contrib import admin
from page.models import Page

# This file specifies some models that interface nicely with django's admin scaffolding
# https://docs.djangoproject.com/en/1.8/ref/contrib/admin/

admin.site.register(Page)