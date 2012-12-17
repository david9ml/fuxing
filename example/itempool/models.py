# coding: utf-8
from django.db import models
from intemass.portal.models import TProfile

'''
Item pools
'''
class Itempool(models.Model):
    poolname = models.CharField(max_length=30, blank=True, null=True,
                                verbose_name='Pool Name')
    teacher = models.ForeignKey(TProfile, verbose_name='Teacher')
    description = models.CharField(max_length=100, blank=True, null=True,
                                   verbose_name='Description')

    class Meta:
        verbose_name = u'Item Pool'

    def __unicode__(self):
        return u'[Itempool:%s]' % self.poolname
