from django.shortcuts import render
from newsletter.models import Message

from django.views.generic import View
class SubmissionArchiveDetailOverrideView(View):
	def get(self, request, newsletter_slug, year, month, day, slug):
		themessage = Message.objects.get(slug=slug)
		return render(request,'newsletter/message/message_online.html', {"message": themessage, "newsletter": themessage.newsletter})