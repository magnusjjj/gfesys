from django.conf.urls import patterns, url


from server import views

urlpatterns = patterns('',
    url(r'^$', views.ViewIndex.as_view(), name='index'),
	url(r'^(?P<server_id>\d+)/$', views.ViewDetail.as_view(), name='detail'),
	url(r'^volunteer/(?P<server_id>\d+)/$', views.ViewVolunteerFor.as_view(), name='volunteer'),
	url(r'^editserver/(?P<server_id>\d+)/$', views.EditServer.as_view(), name='editserver'),
	url(r'^managevolunteers/(?P<server_id>\d+)/$', views.ViewManageVolunteers.as_view(), name='managevolunteers'),
	url(r'^servereditapplicant$', views.ServerEditApplicant.as_view(), name='servereditapplicant'),
	url(r'^serverviewanswers$', views.ServerViewAnswers.as_view(), name='serverviewanswers'),
	url(r'^uploadserverimage/(?P<server_id>\d+)/$', views.UploadServerImage.as_view(), name='uploadserverimage'),
	url(r'^updateserverinfo/(?P<server_id>\d+)/$', views.UpdateServerInfo.as_view(), name='updateserverinfo'),
)
