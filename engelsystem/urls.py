from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('angelsystem.views',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^shifts/(?P<date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})?', 'shifts'),
	url(r'^my-shifts/', 'myShifts'),
	url(r'^$', 'index')
)
