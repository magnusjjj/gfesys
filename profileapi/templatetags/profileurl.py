from django import template
from django.core.urlresolvers import reverse
from server.models import Server

register = template.Library()

@register.simple_tag(takes_context=True)
def profileurl(context, adress, *args, **kwargs):
	if context["profilemodel"].__name__ == "Server":
		return reverse("server:profile:"+adress, args=args, kwargs=kwargs)
	else:
		raise NameError("Unknown type. Check profileapi/templatetags/profileurl.py")
