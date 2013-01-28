import logging
from django.shortcuts import render_to_response
from django.template import RequestContext
from fuxing.activity.models import Activity

logger = logging.getLogger(__name__)

def info(request):
    if request.method == "POST":
        return render_to_response('activity_info.html', context_instance=RequestContext(request))
    else:
        activity_id = request.GET.get('id')
        print "!!!!!!!!!!!!!!!!"+str(activity_id)
        activity = Activity.objects.get(id=activity_id)
        txt_intro = activity.txt_intro.replace('\n', '</br>')
        return render_to_response('activity_info.html', {'activity': activity, 'txt_intro': txt_intro}, context_instance=RequestContext(request))

def admin(request):
    return render_to_response('activity_admin.html', context_instance=RequestContext(request))

def activity(request):
    return render_to_response('activity.html', context_instance=RequestContext(request))

def getall_activities(request):
    logger.info("Getting all activities")
    activities = Activity.objects.all()
    print activities
    for a in activities:
        print a.date
    response = render_to_response('getall_activities.json',
                                  {'activities': activities},
                                  context_instance=RequestContext(request))
    response['Content-Type'] = 'text/plain; charset=utf-8'
    response['Cache-Control'] = 'no-cache'
    return response




'''
import logging
from intemass.classroom.models import Classroom
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from intemass.portal.models import SProfile
from intemass.classroom.forms import ClassDetailForm
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from portal.common import getTpByRequest
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.utils import simplejson

logger = logging.getLogger(__name__)


def __getGroupName(request):
    groups = request.user.groups.all()
    if groups and len(groups) > 0:
        return groups[0].name
    else:
        return None


def __getClassroom(classid, isCreate=False):
    if classid is None or classid == "-1":
        if isCreate:
            return Classroom.objects.create()
        else:
            return None
    return Classroom.objects.get(id=int(classid))


@permission_required('auth.add_user')
def getall(request):
    logger.info("get classroom entry")
    tp, res = getTpByRequest(request, "login")
    if not tp and res:
        return res
    logger.info("tp:%s" % tp)
    try:
        classrooms = tp.classrooms.all()
    except:
        classrooms = []
    logger.info("tp classrooms:%s" % classrooms)
    response = render_to_response('classroom_all.json',
                                  {'classrooms': classrooms},
                                  context_instance=RequestContext(request))
    response['Content-Type'] = 'text/plain; charset=utf-8'
    response['Cache-Control'] = 'no-cache'
    return response


@permission_required('auth.add_user')
def add(request):
    tp, res = getTpByRequest(request, "login")
    if not tp and res:
        return res
    if request.method == 'POST':
        form = ClassDetailForm(request.POST, teacher=tp)
        if form.is_valid():
            classid = form.cleaned_data['classid']
            roomname = form.cleaned_data['classname']
            volume = form.cleaned_data['volume']
            students = form.cleaned_data['stulist']
            classroom = __getClassroom(classid, True)
            classroom.roomname = roomname
            classroom.volume = volume
            logger.info("classid:%s,classroom:%s,students:%s" % (classid, classroom, students))
            #add remove student from classroom
            __updatestuinclassroom(tp, students, classroom)
            classroom.save()
            tp.classrooms.add(classroom)
            messages.add_message(request, messages.SUCCESS,
                                 "%d students has been added to Class %s" % (len(students), classroom.roomname))
            return redirect('/classroom/add?classid=' + str(classroom.id))
        else:
            return render_to_response('classroom_detail.html', {'form': form},
                                      context_instance=RequestContext(request))
    else:
        classid = request.GET.get('classid')
        classroom = __getClassroom(classid)
        logger.info("classroom:%s" % classroom)
        if classid:
            classid_str = str(classid)
        else:
            classid_str = '-1'
        if classroom:
            classname = classroom.roomname
            volume = classroom.volume
        else:
            classname = 'New Class'
            volume = ""
        form = ClassDetailForm(teacher=tp,
                               initial={'classid': classid_str,
                                        'classname': classname, 'volume': volume})
        return render_to_response('classroom_detail.html', {'form': form},
                                  context_instance=RequestContext(request))


def __updatestuinclassroom(teacher, students, classroom):
    try:
        sp = SProfile.objects.filter(teacher=teacher, classroom__in=[classroom, None])
    except Exception, e:
        print e
    else:
        temp = []
        for s in sp:
            if s not in students:
                s.classroom = None
                s.save()
                temp.append(s)
        for stu in students:
            if stu not in temp:
                stu.classroom = classroom
                stu.save()


@permission_required('auth.add_user')
def getstudents(request):
    if request.method == "POST":
        teacher, res = getTpByRequest(request, "login")
        classid = request.POST['classid']
        try:
            view = request.POST['view']
        except:
            view = 0
        logger.info("classid:%s" % classid)
        if classid and classid != '':
            try:
                classroom = Classroom.objects.get(id=int(classid))
            except:
                classroom = None
        else:
            classroom = None
        logger.info("class:%s" % classroom)
        logger.info("teacher:%s" % teacher)

        stu_teacher_list = []
        if not teacher:
            messages.add_message(request, messages.SUCCESS, "%s has no permission" % request.user.username)
        else:
            checkedteachers = []
            if classroom:
                checkedteachers = classroom.tprofile_set.all()
            else:
                checkedteachers.append(teacher)
            logger.info("checkedteacher:%s" % checkedteachers)
            if teacher not in checkedteachers:
                messages.add_message(request, messages.SUCCESS,
                                     "%s has no permission to this classroom:%s"
                                     % (request.user.username, classroom))
            else:
                stu_teacher_list.append(__buildstuofteachertree(teacher, classroom, view))
        response = render_to_response('classroom_getstudents.json',
                                      {'stu_teacher_list': stu_teacher_list,
                                       'tnum': len(stu_teacher_list)},
                                      context_instance=RequestContext(request))
        response['Content-Type'] = 'text/plain; charset=utf-8'
        response['Cache-Control'] = 'no-cache'
        return response


def __buildstuofteachertree(teacher, classroom, view):
    students = SProfile.objects.filter(teacher=teacher)
    logger.info("students:%s" % students)
    teachernode = {'name': teacher.user.username, 'checked': 'true'}
    if view:
        teachernode['disabled'] = 'true'
    else:
        teachernode['disabled'] = 'false'
    studentnodes = []
    for s in students:
        studentnode = {'node': s, 'gender': s.gender, 'sid': s.user.id, 'disabled': 'false'}
        if s.classroom and s.classroom == classroom:
            studentnode['checked'] = 'true'
        elif not s.classroom:
            studentnode['checked'] = 'false'
        else:
            studentnode['disabled'] = 'true'
            studentnode['checked'] = 'false'
        if view:
            studentnode['disabled'] = 'true'
        studentnodes.append(studentnode)
    return [teachernode, studentnodes]


class ClassroomDelete(DeleteView):
    model = Classroom
    success_url = reverse_lazy("deleteview_callback")

    def get_object(self):
        try:
            pk = self.request.POST['classroomid']
        except:
            return None
        return get_object_or_404(Classroom, id=pk)


def classroom_updatename(request):
    logger.info("classroom_updatename...")
    tp, res = getTpByRequest(request, None)
    response_data = {'state': 'failure'}
    if tp:
        classid = request.GET.get("classid").strip()
        roomname = request.GET.get("roomname").strip()
        logger.info("classid:%s,name:%s" % (classid, roomname))
        if classid and roomname and roomname != "":
            if classid == '-1':
                classroom = __getClassroom(classid, True)
                classroom.roomname = roomname
                classroom.save()
                tp.classrooms.add(classroom)
                tp.save()
            else:
                classroom = __getClassroom(classid, False)
                logger.info(" get classroom %s" % classroom)
            if classroom:
                classroom.roomname = roomname
                classroom.save()
                response_data['classid'] = classroom.id
                response_data['roomname'] = classroom.roomname
                response_data['state'] = 'success'
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
'''
