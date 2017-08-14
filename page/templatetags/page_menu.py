# (c) 2015 Magnus "Tuxie" Johnsson, magnusjjj@gmail.com
# Licensed under the BSD license, see LICENSE.TXT in the root folder.
# Revision 1
# Changelog:
# 2015-04-14 - Magnus Johnsson - Added the license header

from django import template
from page.models import Page
register = template.Library()

# This registers a templatetag named 'page_menu'.
# It renders a nice little menu of all the pages. Very simplistic and very placeholder-ish. Needs fleshing out.

class page_menuNode(template.Node):
    def __init__(self):
        pass
    def render(self, context):
		newcontext = {}
		# Get the template to render
		t = template.loader.get_template('page_menu.html')
		# Get a page list
		newcontext["pages"] = Page.objects.filter(parent_content_type=None, parent_object_id=None, type="")
		newcontext["user"] = context["user"]
		# Check if we are proccessing a page...
		if "page" in context:
			newcontext["page"] = context["page"]
		# Render it!
		return t.render(newcontext)

# The code below registers the templatetag to django.
def do_page_menu(parser, token):
	return page_menuNode()

register.tag('page_menu', do_page_menu)