from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def profileurl(context, adress, *args, **kwargs):
	if context["profilemodel"].__name__ == "Server":
		return reverse("server:profile:"+adress, args=args, kwargs=kwargs)
	if context["profilemodel"].__name__ == "GfeGroup":
		return reverse("gfegroups:profile:"+adress, args=args, kwargs=kwargs)

	raise NameError("Unknown type. Check profileapi/templatetags/profileurl.py")
