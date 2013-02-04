# coding: utf-8
from django.db import models
from fuxing.portal.models import Customer
import datetime

class Room(models.Model):
    roomname = models.CharField(max_length=30, verbose_name='RoomName')
    volume = models.IntegerField(blank=True, null=True, verbose_name='Volume')
    date_created = models.DateTimeField('date created', default=datetime.datetime.now)
    pic_intro = models.CharField(max_length=30, verbose_name='Pic_introduction')
    txt_intro = models.CharField(max_length=30, verbose_name='txt_introduction')

    class Meta:
        verbose_name = u'房间'
        verbose_name_plural = u'房间'
        app_label = "room"
        ordering = ['-date_created']

    def __unicode__(self):
        return u'[Room:%s]' % self.roomname

class Reservation(models.Model):
    #assignmentname = models.CharField(max_length=20, verbose_name=u'Assignment Name')
    customer = models.ForeignKey(Customer, verbose_name=u'Customer')
    room = models.ForeignKey(Room, verbose_name=u'Room')
    date_created = models.DateTimeField('reservation date', default=datetime.datetime.now)
    begin_date = models.DateTimeField('begin date', blank=True, null=True)
    end_date = models.DateTimeField('end date', blank=True, null=True)
    deadline = models.DateTimeField('reservation deadline', blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u'Description')

    class Meta:
        verbose_name = u'预定'
        verbose_name_plural = u'预定'
        app_label = "room"
        ordering = ['-date_created']

    def __unicode__(self):
        return u'%s, %s, %s' % (self.id, self.room ,self.customer)
