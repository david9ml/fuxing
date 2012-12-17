from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, Group,Permission
from intemass.portal.models import TProfile,SProfile
from intemass.question.models import Question
from intemass.itempool.models import Itempool
from django.utils.datastructures import MultiValueDictKeyError
import traceback
import logging

class QuestionTest(TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        add_groups_data()
        add_user_data()
        self.client=Client()

    def test_alllinks(self):

        #LOGIN STATE  as teacher
        self.assertTrue(self.client.login(username='weiyan', password='1'))

        #add page
        response = self.client.get('/question/add/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/question/add/?questionid=1&itempoolid=1')
        self.assertEqual(response.status_code,200)

        #imageupload page
        response = self.client.get('/question/imageupload/')
        self.assertEqual(response.status_code,200)

        #updatename page
        response = self.client.get('/question/updatename/')
        self.assertEqual(response.status_code,200)

        #submit page
        response = self.client.post('/question/submit/',
                                    {'questionid':1,'itempoolid':1},
                                    follow = True)
        self.assertEqual(response.status_code,200)

        try:
            response = self.client.post('/question/submit/', follow= False )
        except MultiValueDictKeyError:
            self.logger.info("Passing MultiValueDictKeyError")
        else:
            self.assertTrue(False)
            traceback.print_exc()

        #submit standard  page
        response = self.client.post('/question/submitstandard/',
                                    {'questionid':1, 'standard_content': 'standard'},
                                    follow = True)
        self.assertEqual(response.status_code,200)

        try:
            response = self.client.post('/question/submitstandard/', follow= False )
        except MultiValueDictKeyError:
            self.logger.info("Passing MultiValueDictKeyError")
        else:
            self.assertTrue(False)
            traceback.print_exc()

        #get question  page
        response = self.client.get('/question/get/')
        self.assertEqual(response.status_code,200)

        #submit mark page
        response = self.client.post('/question/submitmark/',
                                    {'questionid':1, 'schemes': 'flock'},
                                    follow = True)
        self.assertEqual(response.status_code,200)

        try:
            response = self.client.post('/question/submitmark/', follow= False )
        except MultiValueDictKeyError:
            self.logger.info("Passing MultiValueDictKeyError")
        else:
            self.assertTrue(False)
            traceback.print_exc()

        #get question  page
        response = self.client.get('/question/get/')
        self.assertEqual(response.status_code,200)

        #question thumbnail  page
        response = self.client.get('/question/thumbnails/')
        self.assertEqual(response.status_code,200)

        #delete image page
        response = self.client.get('/question/deleteimage/')
        self.assertEqual(response.status_code,200)

        #LOGOUT STATE
        self.client.logout()

        #LOGIN STATE  as student
        self.assertTrue(self.client.login(username='w1', password='1'))

        #stuget question  page
        response = self.client.get('/question/stuget/')
        self.assertEqual(response.status_code,200)

        #stu question thumbnail  page
        response = self.client.get('/question/studentthumbnails/')
        self.assertEqual(response.status_code,200)

        #delete image page
        response = self.client.post('/question/deleteimage/',
                                    {'imageid':'34'},follow=True)
        self.assertEqual(response.status_code,200)

        try:
            response = self.client.post('/question/deleteimage/', follow= False )
        except:
            traceback.print_exc()

        self.logger.info("test_alllinks finished")

def add_groups_data():
    try:
        tg = Group.objects.create(name="teachers")
        sg = Group.objects.create(name="students")
    except:
        return

    p1=Permission.objects.get(codename="add_user")
    p2=Permission.objects.get(codename="change_user")
    p3=Permission.objects.get(codename="delete_user")
    p4=Permission.objects.get(codename="add_session")
    p5=Permission.objects.get(codename="change_session")
    p6=Permission.objects.get(codename="delete_session")
    tg.permissions.add(p1)
    tg.permissions.add(p2)
    tg.permissions.add(p3)
    tg.permissions.add(p4)
    tg.permissions.add(p5)
    tg.permissions.add(p6)
    sg.permissions.add(p4)
    sg.permissions.add(p5)
    sg.permissions.add(p6)

def add_user_data():
    weiyan=User.objects.create_user("weiyan","yan,wei_sjtu@yahoo.cn","1")
    weiyantp=TProfile.objects.create(user=weiyan,gender="male",cellphone="13671670930")
    w1=User.objects.create_user("w1","yan,wei_sjtu@yahoo.cn","1")
    w1sp=SProfile.objects.create(user=w1,gender="male",cellphone="13671670930",teacher=weiyantp)
    return weiyantp

def add_question_data(teacher):
    i1 = Itempool.objects.create(poolname='i1', teacher= teacher)
    q1 = Question.objects.create(qname='q1', itempool = i1, teacher = teacher)
    return q1

