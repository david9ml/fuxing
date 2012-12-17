from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('intemass.report.views',
    url(r'^teacher/$', 'report_teacher', name='report_teacher'),
    url(r'^student/$', 'report_student', name='report_student'),
    url(r'^studentanswer/$', 'report_studentanswer', name='report_studentanswer'),
    url(r'^question/$', 'report_question', name='report_question'),
    #url(r'^classroom/$','report_classroom', name='report_classroom'),
	)

