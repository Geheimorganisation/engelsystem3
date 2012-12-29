from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('angelsystem.views',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^shifts/(?P<date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})?', 'shifts'),
	url(r'^my-shifts/', 'my_shifts'),
	url(r'^$', 'index')
)

urlpatterns += patterns('',
	url(settings.LOGOUT_URL[1:], 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(settings.LOGIN_URL[1:], 'django.contrib.auth.views.login', {'template_name': 'login.html'})
)
