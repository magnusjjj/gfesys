from django import template
from django.template import Context
from page.models import Page
register = template.Library()

class page_menuNode(template.Node):
    def __init__(self):
        pass
    def render(self, context):
		t = template.loader.get_template('page_menu.html')
		pages = Page.objects.filter(parent_content_type=None, parent_object_id=None, type="_generic_page")
		return t.render(Context({"pages": pages}))

def do_page_menu(parser, token):
	return page_menuNode()

register.tag('page_menu', do_page_menu)