# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType, ContentTypeManager

from . import register
from spirit.models.topic import Topic
from spirit.models.category import Category

@register.inclusion_tag('spirit/topic_other/topic_list.html', takes_context=True)
def forum_other(context, object):
	content_t = ContentType.objects.get_for_model(object)
	context["objectid"] = object.pk
	context["typeid"] = content_t.pk

	topics = Topic.objects.for_public().filter(other_category_content_type=content_t, other_category_id=object.pk)
	topics = topics.order_by('-is_pinned', '-last_active').select_related('category')
	categories = Category.objects.for_parent()

	context["categories"] = categories
	context["topics"] = topics
	return context
