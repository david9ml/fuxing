from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('fuxing.activity.views',
    url(r'^info/$|^info/cn/$','info',name='info'),
    url(r'^admin/$|^admin/cn/$','admin',name='admin'),
    url(r'^$|^cn/$','activity',name='activity'),
	)

