from django.utils.decorators import classonlymethod
from django.views.generic import View

class ProfileView(View):
	context = {}
	profilemodel = None

	@classonlymethod
	def as_view(cls, **kwargs):
		context = {}
		context["profilemodel"] = kwargs["profilemodel"]
		kwargs["context"] = context
		return super(ProfileView, cls).as_view(**kwargs)
