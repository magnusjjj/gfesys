from django.conf.urls import patterns, url


from member import views

urlpatterns = patterns('',
	url(r'^register$', views.register, name='register'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^login_post$', views.login_post, name='login_post'),
	url(r'^forgot_post$', views.forgot_post, name='forgot_post'),
	url(r'^register_post$', views.register_post, name='register_post'),
)
