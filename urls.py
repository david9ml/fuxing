from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
                       url(r'^portal/', include('fuxing.portal.urls')),
                       url(r'^activity/', include('fuxing.activity.urls')),
                       url(r'^room/', include('fuxing.room.urls')),
                       )

#home
urlpatterns += patterns('fuxing.portal.views',
                       url(r'^$|^cn/$','home', name='home'),
                      )


