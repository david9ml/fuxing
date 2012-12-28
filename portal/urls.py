from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('fuxing.portal.views',
    url(r'^home/$','home', name='home'),
)
