# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from ..utils.forms import NestedModelChoiceField
from spirit.models.category import Category

from spirit.models.topic import Topic
from django.contrib.contenttypes.models import ContentType, ContentTypeManager

class TopicOtherForm(forms.ModelForm):
	
	class Meta:
		model = Topic
		fields = ('title',)

	def __init__(self, user, other_category_id, other_category_content_type, *args, **kwargs):
		super(TopicOtherForm, self).__init__(*args, **kwargs)
		self.user = user
		self.other_category_id = other_category_id
		self.category_id = settings.ST_OTHER_CATEGORY_PK
		self.other_category_content_type = ContentType.objects.get_for_id(other_category_content_type)
		# TODO: add custom Prefetch object to filter closed sub-categories, on Django 1.7

		if self.instance.pk and not user.is_moderator:
			del self.fields['category']

	def save(self, commit=True):
		if not self.instance.pk:
			self.instance.user = self.user
			self.instance.category_id = settings.ST_OTHER_CATEGORY_PK
			self.instance.other_category_id = self.other_category_id
			self.instance.other_category_content_type = self.other_category_content_type

		return super(TopicOtherForm, self).save(commit)
