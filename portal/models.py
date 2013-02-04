# coding: utf-8
from django.db import models
from django.contrib.auth.models import User, Group
import datetime

class Customer(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='UserID')
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name='Gender')
    phone = models.CharField(default='', max_length=16, blank=True, null=True, verbose_name='Cellphone')
    cellphone = models.CharField(default='', max_length=16, blank=True, null=True, verbose_name='Cellphone')
    addition = models.CharField(max_length=500, blank=True, null=True, verbose_name='Addition')
    date_created = models.DateTimeField('customer created date', default=datetime.datetime.now)

    class Meta:
        verbose_name = u'客户'
        verbose_name_plural = u'客户'
        app_label = "portal"
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        self.user.groups = (Group.objects.get(name = 'customer'),)
        super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'[Customer:%s]' % self.user.username

