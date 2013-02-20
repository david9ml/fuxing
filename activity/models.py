# coding: utf-8
from django.db import models
#from fuxing.portal.models import Customer
import datetime

class Activity(models.Model):
    activityname = models.CharField(max_length=200, verbose_name='ActivityName')
    date_created = models.DateTimeField('date', default=datetime.datetime.now)
    pic_intro = models.CharField(max_length=50, verbose_name='Pic_introduction', null=True, blank=True)
    url_link = models.CharField(max_length=50, verbose_name='Url_link', null=True, blank=True)
    txt_intro = models.TextField(max_length=100, verbose_name='txt_introduction', null=True, blank=True)
    addition = models.TextField(max_length=200, verbose_name='addition', null=True, blank=True)

    class Meta:
        verbose_name = u'活动'
        verbose_name_plural = u'活动'
        app_label = "activity"
        ordering = ['-date_created']

    def __unicode__(self):
        return u'[Activity:%s]' % self.activityname

