import logging
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required, login_required
from intemass.paper.models import Paper
from intemass.student.models import StudentAnswer
from intemass.question.models import Question
from intemass.paper.forms import PaperSearchForm
from intemass.report.forms import DetailSearchForm
from portal.common import getSpByRequest, getGroupNameByRequest
from portal.models import SProfile
import re
from django.utils import simplejson as json

logger = logging.getLogger(__name__)


@permission_required('auth.add_user')
def report_teacher(request):
    group = getGroupNameByRequest(request)
    if group != 'teachers':
        return redirect('teacher_index')
    form = PaperSearchForm()
    if request.method == 'POST':
        pids = request.POST.get('paperids')
        return render_to_response('report_paper.html',
                                  {'form': form, 'pids': pids},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('report_teacher.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))


@login_required
def report_studentanswer(request):
    form = []
    group = getGroupNameByRequest(request)
    if request.method == "POST":
        #get table list of all found papers
        paperids = request.POST.get('paperids')
        pids = []
        stuids = []
        if paperids:
            try:
                paper_stu = re.findall(r'\{pid\:(\d+)\,\sstuid\:(\d+)\}', paperids)
            except Exception, e:
                print e
            for pid, stuid in paper_stu:
                pids.append(int(pid))
                stuids.append(int(stuid))
            form = DetailSearchForm(paper=pids, student=stuids)
            return render_to_response('report_studentanswer.html',
                                      {'form': form,
                                       'group': group,
                                       'pids': json.dumps(pids),
                                       'stuids': json.dumps(stuids)},
                                      context_instance=RequestContext(request))
        else:
            try:
                pids = [int(id) for id in request.POST.get('pids').strip('[]').split(',')]
                stuids = [int(id) for id in request.POST.get('stuids').strip('[]').split(',')]
                form = DetailSearchForm(request.POST, paper=pids, student=stuids)
            except Exception, e:
                print e
            if form and form.is_valid():
                student = form.cleaned_data['student']
                paper = form.cleaned_data['paper']
            else:
                if not stuids or not pids:
                    return HttpResponse("students or papers do not exist")
                logger.info("stuids[0]:%s,pids[0]:%s ok!" % (stuids[0], pids[0]))
                try:
                    student = SProfile.objects.get(user__id=stuids[0])
                    paper = Paper.objects.get(id=pids[0])
                except Exception, e:
                    print e
                    student = None
                    paper = None
            return render_to_response('report_studentanswer.html',
                                      {'form': form, 'student': student,
                                       'group': group, 'paper': paper,
                                       'pids': json.dumps(pids),
                                       'stuids': json.dumps(stuids)},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('report_studentanswer.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))


@login_required
def report_question(request):
    questionid = request.GET.get('questionid')
    student, res = getSpByRequest(request, None)
    logger.info(student)
    try:
        question = Question.objects.get(id=questionid)
        studentanswer = StudentAnswer.objects.get(student=student,
                                                  question=question)
        mark = studentanswer.mark
    except:
        return HttpResponse('cant find the specified answer')
    p = re.compile('\'(.*?)\'')
    pointmarklist = []
    try:
        pointmarklist = p.findall(studentanswer.pointmarklist)
    except:
        logger.info("can\'t find pointmark for studentanswer %s" % question.qname)
    pointlist = []
    if pointmarklist:
        for point in pointmarklist:
            pl = 'P' + point
            pointlist.append(pl)
    #p = re.compile('\[\'(.*?)\'')
    omittedpoint = []
    try:
        omittedpoint = p.findall(studentanswer.omitted)
    except:
        logger.info("can\'t find omittedpoint for studentanswer %s" % question.qname)
    omittedlist = []
    if omittedpoint:
        for o in omittedpoint:
            ol = 'P' + o
            omittedlist.append(ol)
    return render_to_response('report_question.html',
                              {'qid': question.id,
                              'mark': mark,
                              'pointmarklist': pointlist,
                              'omittedlist': omittedlist},
                              context_instance=RequestContext(request))


@login_required
def report_student(request):
    group = getGroupNameByRequest(request)
    if group != 'students':
        return redirect('student_index')
    form = PaperSearchForm()
    return render_to_response('report_paper.html',
                              {'form': form},
                              context_instance=RequestContext(request))
