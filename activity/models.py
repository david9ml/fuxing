# coding: utf-8
from django.db import models
#from fuxing.portal.models import Customer
import datetime

class Activity(models.Model):
    activityname = models.CharField(max_length=30, verbose_name='ActivityName')
    date = models.DateTimeField('date', default=datetime.datetime.now)
    pic_intro = models.CharField(max_length=30, verbose_name='Pic_introduction', null=True, blank=True)
    txt_intro = models.TextField(max_length=100, verbose_name='txt_introduction', null=True, blank=True)
    addition = models.TextField(max_length=200, verbose_name='addition', null=True, blank=True)

    class Meta:
        verbose_name = 'Activity'

    def __unicode__(self):
        return u'[Activity:%s]' % self.activityname

