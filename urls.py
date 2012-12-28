from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
                       url(r'^portal/', include('fuxing.portal.urls')),
                       )

urlpatterns = patterns('fuxing.portal.views',
                       url(r'^$','home', name='home'),
                      )
'''
#portal
urlpatterns += patterns('fuxing.portal.views',
                        url(r'^$', 'login', name='login'),
                        url(r'^home/$', 'index', name='index'),
                        url(r'^accounts/register/$', 'register', name='register'),
                        url(r'^accounts/login/$', 'login', name='login'),
                        url(r'^accounts/logout/$', 'logout', name='logout'),
                        url(r'^accounts/forgot-password/$', 'forgot_password', name='forgot_password'),
                        url(r'^accounts/info-modify/$', 'info_modify', name='info_modify'),
                        )
'''
