# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import patterns, url


urlpatterns = patterns("spirit.views.other",
                       url(r'^publish/(?P<other_type_id>\d+)/(?P<other_object_id>\d+)/$', 'other_publish', name='other_publish'),
)
