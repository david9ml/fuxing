from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
#from django.utils.html import strip_tags
#import random
#import pickle
#import os
from fuxing.portal.models import Customer
#from datetime import timedelta, datetime
#from docx import opendocx, getdocumenttext

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'add some test data'

    def handle(self, *args, **options):
        wangping=User.objects.create_user("wangping","wangping@yahoo.cn","wangping")
        wangping_customer = Customer.objects.create(user=wangping, gender="female", cellphone="13611722769", addition="Room609 4 days")
        try:
            wangping_customer.save();
        except:
            pass
        self.stdout.write('Add test data successfully\n')
