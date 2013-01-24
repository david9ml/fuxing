from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('fuxing.room.views',
    url(r'^listall/$|^listall/cn/$','listall',name='listall'),
    url(r'^reserve/$|^reserve/cn/$','roomsreserve',name='reserve'),
    #url(r'^delete/$',ClassroomDelete.as_view(),name='classroom_delete'),
	)

