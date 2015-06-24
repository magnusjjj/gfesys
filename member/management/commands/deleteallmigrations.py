# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django.core.management.base import BaseCommand, CommandError
from spirit.models.category import Category
from spirit.models.topic import Topic
from spirit.models.comment import Comment
from member.models import Member
from server.models import Server, Volunteer
from gfe.settings import *
import os
# Todo: Password for users
# empty database tables?

class Command(BaseCommand):
	args = ''
	help = 'Deletes all migrations'
	
	def handle(self, *args, **options):
		os.system("find . -path \"*/migrations/*.py\" -not -name \"__init__.py\" -exec /usr/bin/git rm -f $1 {} \\;")
		os.system("find . -path \"*/migrations/*.py\" -not -name \"__init__.py\" -delete")
		return
