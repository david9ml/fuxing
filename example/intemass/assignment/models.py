# coding: utf-8
from django.db import models
from intemass.portal.models import TProfile,SProfile
import datetime

class Assignment(models.Model):
    assignmentname = models.CharField(max_length=20, verbose_name=u'Assignment Name')
    description = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u'Description')
    students = models.ManyToManyField(SProfile, blank=True, null=True,verbose_name=u'Students')
    teacher = models.ForeignKey(TProfile, verbose_name=u'Teacher')
    date_created = models.DateTimeField('test date', default=datetime.datetime.now)
    deadline = models.DateTimeField('test deadline', blank=True, null=True)

    class Meta:
        verbose_name = u'Assignment'

    def __unicode__(self):
        return u'%s' % self.assignmentname