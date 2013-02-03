from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('fuxing.portal.views',
    url(r'^home/$|^home/cn/$','home', name='home'),
    url(r'^contacts/$|^contacts/cn/$','contacts', name='contacts'),
    url(r'^partners/$|^partners/cn/$','partners', name='partners'),
)
