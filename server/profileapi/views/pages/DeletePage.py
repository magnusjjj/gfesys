from django.shortcuts import redirect

from page.models import Page
from server.models import Server


class DeletePage:
	def get(self, request, page_id):
		super(DeletePage, self).get(request)
		context = {}
		# Fetch Page
		page = Page.objects.get(pk=page_id)

		if type(page.parent) is Server:
			# Fetch the server
			context["server"] = page.parent

			# Fetch our access rights
			self.setrights_server(request, context, page.parent.pk)

			# Security sanity check that we have edit rights
			if request.user.is_administrator or context["volunteer"].sec_edit:
				page.delete()
				return redirect(page.parent)