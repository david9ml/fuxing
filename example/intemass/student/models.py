from django.db import models
from intemass.portal.models import SProfile
from intemass.question.models import Question, QuestionImage


class StudentAnswer(models.Model):
    student = models.ForeignKey(SProfile)
    sentencelist = models.TextField(null=True, blank=True)
    mark = models.IntegerField(default=0)
    historymarklist = models.TextField(null=True, blank=True)
    pointmarklist = models.TextField(null=True, blank=True)
    omitted = models.TextField(null=True, blank=True)
    html_answer = models.TextField(null=True, blank=True)
    txt_answer = models.TextField(null=True, blank=True)
    question = models.ForeignKey(Question)
    timeleft = models.IntegerField(default=-1)
    taked = models.BooleanField(verbose_name=u'Question Taked')
    stuansimages = models.ManyToManyField(QuestionImage, verbose_name=u'stuansimages')

    def __unicode__(self):
        return u'StudentAnswerSheet_' + str(self.question.qname) + u'_' + self.student.user.username + '-----' + str(self.id)
