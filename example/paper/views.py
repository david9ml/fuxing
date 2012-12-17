import logging
import pickle
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from intemass.paper.models import Paper
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from intemass.paper.forms import PaperDetailForm
from intemass.itempool.models import Itempool
from intemass.question.models import Question
from intemass.student.models import StudentAnswer
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import DeleteView
from portal.common import getTpByRequest, getSpByRequest
from portal.models import SProfile
from django.http import HttpResponse
from django.utils import simplejson
from intemass.assignment.models import Assignment

logger = logging.getLogger(__name__)


@login_required
def getPaperInfoById(request):
    response_data = {'state': 'failure'}
    if request.method == 'POST':
        paperid = request.POST.get("paperid")
        if paperid:
            try:
                paper = Paper.objects.get(id=int(paperid))
                response_data['papername'] = paper.papername
                response_data['duration'] = paper.duration
            except Exception, e:
                print e
            else:
                if paper.assignment:
                    response_data['assignment'] = paper.assignment.assignmentname
                if paper.year:
                    response_data['year'] = paper.year.yearname
                if paper.level:
                    response_data['level'] = paper.level.levelname
                if paper.subject:
                    response_data['subject'] = paper.subject.subjectname
                response_data['state'] = 'success'
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")


@login_required
def paper_getall(request):
    if  request.method == 'POST':
        pids = request.POST.get('pids')
        student, res = getSpByRequest(request, None)
        if pids and not student:
            takedpaperlist = __teachermarkreport(pids)
        elif student:
            takedpaperlist = __studentmarkreport(student)
        logger.info(takedpaperlist)
        response = render_to_response('paper_mark.json', {'takedpaperlist': takedpaperlist},
                                      context_instance=RequestContext(request))
    else:
        forwhat = request.GET.get('forwhat')
        if forwhat == 'teacher_report':
            """
               teacher_report default datatable
            """
            try:
                papers = Paper.objects.filter(owner=request.user)
            except:
                papers = []
            response = render_to_response('paper_report.json',
                                          {'papers': papers},
                                          context_instance=RequestContext(request))
        else:
            """
                teacher get all paper ztree
            """
            try:
                papers = Paper.objects.filter(owner=request.user)
            except:
                papers = []
            response = render_to_response('paper_all.json', {'papers': papers},
                                          context_instance=RequestContext(request))
    response['Content-Type'] = 'text/plain; charset=utf-8'
    response['Cache-Control'] = 'no-cache'
    return response


def __teachermarkreport(pids):
    """
    teacher report post pids
    """
    takedpaperlist = []
    try:
        paperids = [int(i) for i in pids.split(',')]
        papers = Paper.objects.filter(id__in=paperids)
    except Exception, e:
        print e
        papers = []
    for p in papers:
        students = SProfile.objects.filter(assignment=p.assignment)
        for student in students:
            answers = StudentAnswer.objects.filter(student=student, question__in=Question.objects.filter(paper=p), taked=True)
            logger.info(answers)
            if answers:
                mark = sum(ans.mark for ans in answers)
                takedpaperlist.append([p, student, mark])
    return takedpaperlist


def __studentmarkreport(student):
    """
        student report post none
    """
    takedpaperlist = []
    try:
        assignments = Assignment.objects.filter(students=student)
        papers = Paper.objects.filter(assignment__in=assignments)
    except Exception, e:
        print e
        papers = []
    for p in papers:
        answers = StudentAnswer.objects.filter(student=student, taked=True,
                                               question__in=Question.objects.filter(paper=p))
        if answers:
            mark = sum(ans.mark for ans in answers)
            takedpaperlist.append([p, student, mark])
    return takedpaperlist


@permission_required('auth.add_user')
def paper_add(request):
    tp, res = getTpByRequest(request, None)
    if request.method == "POST":
        form = PaperDetailForm(request.POST, teacher=tp)
        if form.is_valid():
            paperid = form.cleaned_data['paperid']
            papername = form.cleaned_data['papername']
            duration = form.cleaned_data['duration']
            passpoint = form.cleaned_data['passpoint']
            year = form.cleaned_data['year']
            subject = form.cleaned_data['subject']
            level = form.cleaned_data['level']
            papertype = form.cleaned_data['ptype']
            if paperid != -1:
                try:
                    paper = Paper.objects.get(id=paperid)
                except:
                    paper = Paper.objects.create(papername=papername,
                                                 passpoint=passpoint,
                                                 ptype=papertype, duration=duration,
                                                 year=year, subject=subject,
                                                 level=level, owner=request.user)
                else:
                    paper.papername = papername
                    paper.ptype = papertype
                    paper.year = year
                    paper.subject = subject
                    paper.level = level
                    paper.duration = duration
                    paper.passpoint = passpoint
            else:
                try:
                    paper = Paper.objects.create(papername=papername,
                                                 passpoint=passpoint,
                                                 ptype=papertype, duration=duration,
                                                 year=year, subject=subject,
                                                 level=level, owner=request.user)
                except:
                    paper = None
            questionlist = form.cleaned_data['questionlist']
            paper.questionseq = pickle.dumps([q.id for q in questionlist])
            paper.total = len(questionlist)
            logger.info("questionlist:%s" % questionlist)
            __updatequestioninpaper(questionlist, paper)
            paper.save()
            messages.add_message(request, messages.SUCCESS, "One Paper Added")
            return redirect("/paper/add?paperid=" + str(paper.id))
    else:
        paperid = request.GET.get('paperid')
        if paperid:
            try:
                p = Paper.objects.get(id=int(paperid))
            except:
                logger.info("paper not found:%s" % paperid)
                form = PaperDetailForm(teacher=tp)
            else:
                logger.info("paper:%s" % p.papername)
                form = PaperDetailForm(teacher=tp,
                                       initial={'paperid': p.id,
                                       'papername': p.papername,
                                       'duration': p.duration,
                                       'passpoint': p.passpoint,
                                       'year': p.year,
                                       'subject': p.subject,
                                       'level': p.level,
                                       'ptype': p.ptype})
        else:
            form = PaperDetailForm(teacher=tp)
    return render_to_response('paper_detail.html', {"form": form},
                              context_instance=RequestContext(request))


def __updatequestioninpaper(questionlist, paper):
    questions = Question.objects.filter(paper=paper)
    temp = []
    for q in questions:
        if q not in questionlist:
            questionseq = pickle.loads(str(q.paper.all()[0].questionseq))
            questionseq.remove(q.id)
            q.paper.remove(paper)
            q.save()
            temp.append(q)
    for q in questionlist:
        if q not in temp:
            q.paper.add(paper)
            q.save()


@login_required
def paper_getquestions(request):
    if request.method == "POST":
        paperid = request.POST['paperid']
        try:
            view = request.POST['view']
        except:
            view = 0
        teacher, res = getTpByRequest(request, None)
        student = None
        if not teacher:
            student, res = getSpByRequest(request, None)
            teacher = student.teacher
        logger.info("paper_getquestions,paperid:%s,teacher:%s" % (paperid, teacher))

        if paperid and paperid != '-1':
            try:
                paper = Paper.objects.get(id=int(paperid))
                questionseq = pickle.loads(str(paper.questionseq))
            except:
                paper = None
                questionseq = []
            if paper and questionseq:
                ztreejson, qnum, checkeditempools = __buildcheckeditempooltree(questionseq, view, student)
                try:
                    totalitempool = Itempool.objects.filter(teacher=teacher)
                    itempools = list(set(totalitempool) - set(checkeditempools))
                except:
                    itempools = []
                else:
                    ztreejson += __builduncheckeditempooltree(itempools, view, student)
        elif paperid == '-1':
            itempools = Itempool.objects.filter(teacher=teacher)
            ztreejson = __builduncheckeditempooltree(itempools, view, student)
            qnum = 0
        else:
            ztreejson = []
            qnum = 0
        response = render_to_response('paper_allquestions.json',
                                      {'questiontree': ztreejson,
                                       'inum': len(ztreejson), 'qnum': qnum},
                                      context_instance=RequestContext(request))
        response['Content-Type'] = 'text/plain; charset=utf-8'
        response['Cache-Control'] = 'no-cache'
        return response


def __buildcheckeditempooltree(questionseq, view, student):
    # for checkeditempools
    checkeditempools = []
    for qid in questionseq:
        try:
            cq = Question.objects.get(id=qid)
        except:
            pass
        else:
            if cq.itempool not in checkeditempools:
                checkeditempools.append(cq.itempool)
    ztreejson = []
    qnum = 0
    for item in checkeditempools:
        questionnodes = []
        itemnode = {'name': item.poolname, 'checked': 'true'}
        if view:
            itemnode['disabled'] = 'true'
        else:
            itemnode['disabled'] = 'false'
        # checkedquestions
        if student:
            checkedquestions = Question.objects.filter(itempool=item, id__in=questionseq,
                                                       qtype="Review")
        else:
            checkedquestions = Question.objects.filter(itempool=item, id__in=questionseq)
        for q in checkedquestions:
            questionnode = {'node': q, 'checked': 'true'}
            if view:
                questionnode['disabled'] = 'true'
            else:
                questionnode['disabled'] = 'false'
            qnum += 1
            questionnodes.append(questionnode)
        #uncheckedquestions
        if student:
            uncheckedquestions = Question.objects.filter(itempool=item,
                                                         infocompleted=Question.ALLCOMPLETED,
                                                         qtype="Review").exclude(id__in=questionseq)
        else:
            uncheckedquestions = Question.objects.filter(itempool=item,
                                                         infocompleted=Question.ALLCOMPLETED).exclude(id__in=questionseq)
        for q in uncheckedquestions:
            questionnode = {'node': q, 'checked': 'false'}
            if view:
                questionnode['disabled'] = 'true'
            else:
                questionnode['disabled'] = 'false'
            questionnodes.append(questionnode)
        ztreejson.append([itemnode, questionnodes])
    return ztreejson, qnum, checkeditempools


def __builduncheckeditempooltree(itempools, view, student):
    # for uncheckeditempools
    ztreejson = []
    for item in itempools:
        questionnodes = []
        itemnode = {'name': item.poolname, 'checked': 'false'}
        if view:
            itemnode['disabled'] = 'true'
        else:
            itemnode['disabled'] = 'false'
        # get question: if request from student, only qtype=Review
        if student:
            questions = Question.objects.filter(itempool=item,
                                                infocompleted=Question.ALLCOMPLETED,
                                                qtype="Review")
        else:
            questions = Question.objects.filter(itempool=item,
                                                infocompleted=Question.ALLCOMPLETED)
        if questions:
            for q in questions:
                questionnode = {'node': q, 'checked': 'false'}
                if view:
                    questionnode['disabled'] = 'true'
                else:
                    questionnode['disabled'] = 'false'
                questionnodes.append(questionnode)
            ztreejson.append([itemnode, questionnodes])
    return ztreejson


class PaperDelete(DeleteView):
    model = Paper
    success_url = reverse_lazy("deleteview_callback")

    def get_object(self):
        pk = self.request.POST['paperid']
        return get_object_or_404(Paper, id=pk)


@permission_required('auth.add_user')
def paper_updatename(request):
    logger.info("paper updatename...")
    tp, res = getTpByRequest(request, None)
    response_data = {'state': 'failure'}
    if tp:
        paperid = request.GET.get('paperid')
        papername = request.GET.get('papername')
        if paperid and papername:
            paper = Paper.objects.get(id=int(paperid.strip()))
            if paper:
                paper.papername = papername
                paper.owner = tp.user
                paper.save()
                response_data['paperid'] = paper.id
                response_data['papername'] = paper.papername
                response_data['ptype'] = paper.ptype
                response_data['duration'] = paper.duration
                response_data['year'] = [paper.year.id, paper.year.yearname]
                response_data['subject'] = [paper.subject.id, paper.subject.subjectname]
                response_data['level'] = [paper.level.id, paper.level.levelname]
                response_data['state'] = 'success'
        elif not paperid:
            paper = paper.objects.create(papername=papername,
                                         ptype='Formal', owner=tp.user)
            response_data['paperid'] = paper.id
            response_data['papername'] = paper.papername
            response_data['state'] = 'success'
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
