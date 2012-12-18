# coding: utf-8

from django.db import models
#from fuxing.portal.models import Customer
#import datetime

class Activity(models.Model):
    activityname = models.CharField(max_length=30, verbose_name='ActivityName')
    pic_intro = models.CharField(max_length=30, verbose_name='Pic_introduction')
    txt_intro = models.CharField(max_length=30, verbose_name='txt_introduction')

    class Meta:
        verbose_name = 'Activity'

    def __unicode__(self):
        return u'[Activity:%s]' % self.activityname

