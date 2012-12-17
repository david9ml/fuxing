import os,sys
import logging
from django import forms
from django.contrib.auth.models import User
from intemass.classroom.models import Classroom
from intemass.question.models import Question
from intemass.paper.models import Paper
sys.path.append(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))))
from portal.common import *
from django.shortcuts import get_object_or_404

logger=logging.getLogger(__name__)

class StudentDetailForm(forms.Form):
    def __init__(self,*args,**kwargs):
        teacher = kwargs.pop('teacher')
        super(StudentDetailForm,self).__init__(*args,**kwargs)
        if teacher:
            classrooms = teacher.classrooms.all()
            cs = [(-1,"---------")]+[(c.id,c.roomname) for c in classrooms]
            self.fields['clazz'] = forms.ChoiceField(choices=cs,label="ClassNo")

    username = forms.CharField(label = 'Account Name',max_length = 30)
    password1 = forms.CharField(label = 'Password', max_length = 30,
                              widget = forms.PasswordInput())
    password2 = forms.CharField(label = 'Password Confirm', max_length = 30,
                              widget = forms.PasswordInput())
    email    = forms.EmailField(label ='Email',max_length = 30)
    clazz    = forms.ChoiceField(required=False)
    gender = forms.ChoiceField(choices=[("male","male"),("female","female")],label ="Gender")

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1=self.cleaned_data['password1']
            password2=self.cleaned_data['password2']
            if password1 == password2:
                if password2 != "":
                    return password2
                else:
                    raise forms.ValidationError('Password cannot be empty')
            else:
                raise forms.ValidationError('Passwords Input don\'t match each other!')

    def clean_username(self):
        users = User.objects.filter(username__iexact = self.cleaned_data['username'])
        if not users:
            return self.cleaned_data['username']
        raise forms.ValidationError('Existed username!')

    def clean_email(self):
        emails = User.objects.filter(email__iexact = self.cleaned_data['email'])
        if not emails:
            return self.cleaned_data['email']
        raise forms.ValidationError('Existed email!')

    def clean_clazz(self):
        clazz = self.cleaned_data['clazz']
        if int(clazz) == -1:
            return None
        else:
            return get_object_or_404(Classroom,id = clazz)

class StudentModifyForm(forms.Form):
    def __init__(self,*args,**kwargs):
        teacher = kwargs.pop('teacher')
        super(StudentModifyForm,self).__init__(*args,**kwargs)
        if teacher:
            classrooms = teacher.classrooms.all()
            cs = [(-1,"-----")] + [(c.id, c.roomname) for c in classrooms]
            self.fields['clazz'] = forms.ChoiceField(choices=cs,label="Classroom ID")

    username = forms.CharField(label = 'Account Name',max_length = 30)
    password1 = forms.CharField(label = 'Password', max_length = 30,
                              widget = forms.PasswordInput())
    password2 = forms.CharField(label = 'Password Confirm', max_length = 30,
                              widget = forms.PasswordInput())
    email    = forms.EmailField(label ='Email',max_length = 30)
    clazz    = forms.ChoiceField(required = False)
    gender = forms.ChoiceField(choices=[("male","male"),("female","female")],label ="Gender")

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1=self.cleaned_data['password1']
            password2=self.cleaned_data['password2']
            if password1 == password2:
                if password2 != "":
                    return password2
                else:
                    raise forms.ValidationError('Password cannot be empty')
            else:
                raise forms.ValidationError('Passwords Input don\'t match each other!')

'''
    def clean_email(self):
        emails = User.objects.filter(email__iexact = self.cleaned_data['email'])
        if not emails:
            return self.cleaned_data['email']
        raise forms.ValidationError('Error email format!')
    '''

class CustomPaperForm(forms.Form):
    def __init__(self,*args,**kwargs):
        owner = kwargs.pop('owner')
        super(CustomPaperForm,self).__init__(*args,**kwargs)
        if owner:
            studentpaper = Paper.objects.filter(owner= owner)
            ps=[(p.id,p.papername) for p in studentpaper]+[(-1,"New Paper")]
            self.fields['paperid'] = forms.ChoiceField(choices=ps,label="Paper ID")

    paperid=forms.ChoiceField(label="Paper ID")
    papername = forms.CharField(max_length = 20, label = 'Paper Name')
    questionlist = forms.CharField(label = 'questionlist')
    duration =forms.CharField(max_length=20,
                              widget=forms.TextInput(attrs={"style":"width:130px;"}))

    def clean_questionlist(self):
        qs=self.cleaned_data['questionlist']
        if ',' in qs:
            qids = qs.split(',')
        else:
            qids= [qs]
        questions=[]
        for q in qids:
            try:
                question=Question.objects.get(id=int(q))
            except:
                continue
            questions.append(question)
        return questions
