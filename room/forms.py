#coding=utf-8
import logging
from django import forms
from fuxing.room.models import Room

logger = logging.getLogger(__name__)

class RoomsreserveForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super(RoomsreserveForm,self).__init__(*args,**kwargs)
        rooms = Room.objects.all()
        rm = [(r.id,r.roomname) for r in rooms]
        self.fields['roomname'] = forms.ChoiceField(choices=rm,label="Roomname")
    #roomname = forms.ChoiceField(choices=rm,label="Roomname")
    begin_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    customer_name = forms.CharField(label = 'customer_name',max_length=30,
            widget = forms.TextInput())
    phone = forms.CharField(label = 'phone',max_length=30,
            widget = forms.TextInput())
    cellphone = forms.CharField(label = 'cellphone',max_length=30,
            widget = forms.TextInput())
    email = forms.EmailField(label = 'cellphone',max_length=30,
            widget = forms.TextInput(),
            error_messages={'required':u'邮箱不能为空', 'invalid':u'请输入有效邮箱'})
    def clean_roomname(self):
        roomname_id = self.cleaned_data['roomname']
        if roomname_id == None:
            raise forms.ValidationError('Invalid roomname!')
        return roomname_id

'''
class ClassDetailForm(forms.Form):
    def __init__(self,*args,**kwargs):
        teacher = kwargs.pop('teacher')
        super(ClassDetailForm,self).__init__(*args,**kwargs)
        if teacher:
            classrooms = teacher.classrooms.all()
            cs = [(-1,"New Class")] + [(c.id,c.roomname) for c in classrooms]
            self.fields['classid'] = forms.ChoiceField(choices=cs,label="ClassNo.")
            self.fields['stulist'].required = False

    classid = forms.ChoiceField(label="ClassNo.")
    classname = forms.CharField(label = "Class Name",max_length = 30)
    volume = forms.CharField(label = "Class Volume",max_length = 30)
    stulist = forms.CharField(label = "stulist")

    def clean_stulist(self):
        stulist = self.cleaned_data['stulist']
        logger.info("stulist:%s" % stulist)
        if stulist == '':
            return []
        elif ',' in stulist:
            studentids = stulist.split(',')
        else:
            studentids = [stulist]
        logger.info("studentids:%s" % studentids)
        students = []
        for sid in studentids:
            logger.info("sid:%s" % sid)
            try:
                student = SProfile.objects.get(user__id=int(sid))
            except:
                continue
            students.append(student)
        return students
'''
