from django.utils.decorators import classonlymethod
from django.views.generic import View

class ProfileView(View):
	context = {}
	profilemodel = None

	@classonlymethod
	def as_view(cls, **initkwargs):
		context = {}
		context["profilemodel"] = initkwargs["profilemodel"]
		initkwargs["context"] = context
		return super(ProfileView, cls).as_view(**initkwargs)
