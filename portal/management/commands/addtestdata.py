from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
#from django.utils.html import strip_tags
#import random
#import pickle
#import os
from fuxing.portal.models import Customer
from fuxing.activity.models import Activity
from fuxing.room.models import Room, Reservation
#from datetime import timedelta, datetime
#from docx import opendocx, getdocumenttext

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'add some test data'

    def handle(self, *args, **options):
        wangping=User.objects.create_user("wangping","wangping@yahoo.cn","1")
        wangping_customer = Customer.objects.create(user=wangping, gender="female", cellphone="13611722769", addition="Room609 4 days")
        rooms = []
        try:
            room1 = Room.objects.create(roomname='room611', volume=50,  pic_intro='/user/pictures/', txt_intro='room_text')
            rooms.append(room1)
            rooms.append(Room.objects.create(roomname='Room601', volume=50,  pic_intro='/user/pictures/', txt_intro='room_text'))
            rooms.append(Room.objects.create(roomname='room609', volume=50,  pic_intro='/user/pictures/', txt_intro='room_text'))
            rooms.append(Room.objects.create(roomname='room612', volume=50,  pic_intro='/user/pictures/', txt_intro='room_text'))
            rooms.append(Room.objects.create(roomname='room613', volume=50,  pic_intro='/user/pictures/', txt_intro='room_text'))
            rooms.append(Room.objects.create(roomname='room619', volume=50,  pic_intro='/user/pictures/', txt_intro='room_text'))
        except:
            pass
        for room in rooms:
            room.save()
        activities = []
        try:
            activities.append(Activity.objects.create(activityname='talk show contest1', pic_intro='/user/pictures', txt_intro='activities_text'))
            activities.append(Activity.objects.create(activityname='talk show contest2', pic_intro='/user/pictures', txt_intro='activities_text'))
            activities.append(Activity.objects.create(activityname='talk show contest3', pic_intro='/user/pictures', txt_intro='activities_text'))
            activities.append(Activity.objects.create(activityname='talk show contest4', pic_intro='/user/pictures', txt_intro='activities_text'))
        except:
            pass
        try:
            wangping_customer.save();
        except:
            pass
        res1 = Reservation.objects.create(customer=wangping_customer, room=room1, description='test')
        res1.save()
        self.stdout.write('Add test data successfully\n')
