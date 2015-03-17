from django import template
from django.template import Context
from page.models import Page
register = template.Library()

class page_tinymceNode(template.Node):
	name = ""
	value =""
	def __init__(self,name,value):
		self.name = name
		self.value = template.Variable(value)
	def render(self, context):
		t = template.loader.get_template('page_tinymce.html')
		content = ""
		try:
			content = self.value.resolve(context)
		except:
			pass
		return t.render(Context({"name": self.name, "value": content}))

def do_page_tinymce(parser, token):
	try:
		tag_name, field_name, value = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError(
			"%r tag requires two arguments " % token.contents.split()[0]
		)
	return page_tinymceNode(field_name[1:-1], value)

register.tag('page_tinymce', do_page_tinymce)