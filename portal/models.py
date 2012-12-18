from django.db import models
from django.contrib.auth.models import User, Group

class Customer(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='UserID')
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name='Gender')
    cellphone = models.CharField(default='', max_length=16, blank=True, null=True, verbose_name='Cellphone')
    addition = models.CharField(max_length=500, blank=True, null=True, verbose_name='Addition')
    class Meta:
        verbose_name = 'customer'
    def save(self, *args, **kwargs):
        self.user.groups = (Group.objects.get(name = 'customer'),)
        super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'[Customer:%s]' % self.user.username

'''
class TProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='UserID')
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name='Gender')
    cellphone = models.CharField(default='', max_length=16, blank=True, null=True,	verbose_name='Cellphone')
    classrooms = models.ManyToManyField(Classroom, verbose_name=u'RelatedClassrooms')
    class Meta:
        verbose_name = 'teacher'

    def save(self, *args, **kwargs):
        self.user.groups = (Group.objects.get(name = 'teachers'),)
        super(TProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'[Teacher:%s]' % self.user.username

class SProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='UserID')
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name='Gender')
    cellphone = models.CharField(default='', max_length=16, blank=True,
                                 null=True,	verbose_name='Cellphone')
    classroom = models.ForeignKey(Classroom, blank=True, null=True,
                                  verbose_name='RelatedClassroom',on_delete=models.SET_NULL)
    teacher = models.ForeignKey(TProfile, blank=True, null=True,
                                 verbose_name='RelatedTeacher',on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'student'

    def save(self, *args, **kwargs):
        self.user.groups = (Group.objects.get(name = 'students'),)
        super(SProfile, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'[Student:%s]' % self.user.username
'''
