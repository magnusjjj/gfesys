# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django import template
from django.template import Context
from page.models import Page
register = template.Library()

# This registers a templatetag named 'page_tinymce'.
# It renders a nice tinymceeditor. Very simplistic and very placeholder-ish. Needs fleshing out.

class page_tinymceNode(template.Node):
	name = ""
	value =""
	def __init__(self,name,value):
		self.name = name
		self.value = template.Variable(value)
	def render(self, context):
		# Get the template to render
		t = template.loader.get_template('page_tinymce.html')
		# Check if we are to fill it with content or leave it blank
		content = ""
		try:
			content = self.value.resolve(context)
		except:
			pass
		
		# Then render!
		return t.render(Context({"name": self.name, "value": content}))


# The code below registers the templatetag to django.
def do_page_tinymce(parser, token):
	try:
		tag_name, field_name, value = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError(
			"%r tag requires two arguments " % token.contents.split()[0]
		)
	return page_tinymceNode(field_name[1:-1], value)

register.tag('page_tinymce', do_page_tinymce)