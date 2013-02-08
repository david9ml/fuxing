from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('fuxing.room.views',
    url(r'^listall/$|^listall/cn/$','listall',name='listall'),
    url(r'^reserve/$|^reserve/cn/$','roomsreserve',name='reserve'),
    url(r'^room_a/$|^room_a/cn/$','room_a',name='room_a'),
    url(r'^room_b/$|^room_b/cn/$','room_b',name='room_b'),
    url(r'^room_c/$|^room_c/cn/$','room_c',name='room_c'),
    url(r'^room_d/$|^room_d/cn/$','room_d',name='room_d'),
    url(r'^room_e/$|^room_e/cn/$','room_e',name='room_e'),
    url(r'^room_small/$|^room_small/cn/$','room_small',name='room_small'),
    url(r'^room_big/$|^room_big/cn/$','room_big',name='room_big'),
    url(r'^room_public/$|^room_public/cn/$','room_public',name='room_public'),
    #url(r'^delete/$',ClassroomDelete.as_view(),name='classroom_delete'),
	)

