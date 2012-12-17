# coding: utf-8
from django.db import models
from intemass.itempool.models import Itempool
from intemass.paper.models import Paper
from intemass.portal.models import TProfile


class StandardAnswer(models.Model):
    name = models.CharField(max_length=50)
    fullmark = models.IntegerField(default=0)
    textfdist = models.TextField()
    sentencelist = models.TextField()
    rulelist = models.TextField(null=True, blank=True)
    imgrulelist = models.TextField(null=True, blank=True)
    pointlist = models.TextField()

    def __unicode__(self):
        return u'StandardAnswer_%s' % self.name


class Question(models.Model):
    QUESTIONCOMPLETED = 1
    STDANSWERCOMPLETED = 2
    MARKSCHEMECOMPLETED = 4
    ALLCOMPLETED = 7
    qname = models.CharField(max_length=30, verbose_name='Question Name')
    description = models.CharField(max_length=1000, verbose_name=u'description',
                                   blank=True, null=True)
    category = models.CharField(max_length=30, verbose_name='category',
                                blank=True, null=True)
    qtype = models.CharField(max_length=20, verbose_name=u'Question Type',
                             blank=True, null=True)
    itempool = models.ForeignKey(Itempool, verbose_name=u'Item Pool')
    paper = models.ManyToManyField(Paper, verbose_name=u'Paper',
                                   blank=True, null=True)
    teacher = models.ForeignKey(TProfile, verbose_name=u'Teacher')
    stdanswer = models.OneToOneField(StandardAnswer, blank=True, null=True,
                                     verbose_name=u'Standard Answer')
    stdanswertext = models.TextField(blank=True, null=True,
                                     verbose_name=u'Standard Answer Text')
    stdanswerhtml = models.TextField(blank=True, null=True,
                                     verbose_name=u'Standard Answer HTML')
    qtext = models.TextField(blank=True, null=True,
                             verbose_name=u'Question Text')
    qhtml = models.TextField(blank=True, null=True,
                             verbose_name=u'Question HTML')
    markscheme = models.TextField(blank=True, null=True,
                                  verbose_name=u'Mark Scheme')
    infocompleted = models.IntegerField(default=0)
    imagepointlist = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = u'Question'

    def __unicode__(self):
        return u'[Question:%s,Category:%s,Type:%s]' % (self.qname, self.category, self.qtype)


class QuestionImage(models.Model):
    imagename = models.CharField(max_length=30, verbose_name=u'Image Name')
    description = models.CharField(max_length=100, verbose_name=u'Description', blank=True, null=True)
    iscorrect = models.BooleanField(verbose_name=u'Is Correct')
    abspath = models.CharField(max_length=50, verbose_name=u'Absulte Path')
    question = models.ForeignKey(Question, verbose_name=u'Question')
    digest = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'md5')

    class Meta:
        verbose_name = u'Question Image'

    def __unicode__(self):
        return u'[Image Name:%s, IsCorrect:%s, Abspath:%s]' % (self.imagename, self.iscorrect, self.abspath)
