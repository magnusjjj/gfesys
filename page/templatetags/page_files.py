# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django import template
from django.template import Context
from page.models import Page
register = template.Library()

# This registers a templatetag named 'page_files'.
# It handles file uploads in the page editor

class page_filesNode(template.Node):
	files =""
	
	def __init__(self,files):
		self.files = template.Variable(files)
		
	def render(self, context):
		# Get the template to render
		t = template.loader.get_template('page_files.html')
		# Check if we are to fill it with content or leave it blank
		files = []
		try:
			files = self.files.resolve(context)
		except:
			pass
		
		# Then render!
		return t.render(Context({"files": files}))


# The code below registers the templatetag to django.
def do_page_files(parser, token):
	try:
		tag_name, files = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError(
			"%r tag requires one argument " % token.contents.split()[0]
		)
	return page_filesNode(files)

register.tag('page_files', do_page_files)