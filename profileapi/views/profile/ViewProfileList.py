from django.shortcuts import render

from profileapi.helpers.ProfileView import ProfileView

# This should... probably not be here. Eheheheh. List of servers.
class ViewProfileList(ProfileView):
	def get(self, request):
		self.context["allow_add"] = self.profilemodel.allow_add(request.user)
		self.context["profiles"] = self.profilemodel.objects.filter().order_by('id')
		# Render that thing right up. Hence why this should not not be here, but, alas, penis.
		return render(request,'profileapi/index.html', self.context)

