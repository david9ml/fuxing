# Create your views here.
import pickle
import logging
from django.utils import simplejson as json
from django.views.generic import TemplateView
from django.http import HttpResponse
from intemass.canvas.models import Canvas
from intemass.question.models import Question
from intemass.student.models import StudentAnswer
from intemass.algo.canvascompare import Canvascompare

logger = logging.getLogger(__name__)


class CanvasView(TemplateView):
    template_name = 'raphael.html'


def canvas_upload(request):
    response_data = {'state': 'failure'}
    if request.method == "POST":
        id = json.loads(request.POST['id'].encode('utf-8'))
        canvasmap = json.loads(request.POST['canvasmap'].encode('utf-8'))
        try:
            question = Question.objects.get(id=id['questionid'])
            stdanswer = None
            stuanswer = None
            if id.get('stdanswerid'):
                stdanswer = question.stdanswer
            elif id.get('stuanswerid'):
                stuanswer = StudentAnswer.objects.get(id=id['stuanswerid'])
        except Exception, e:
            logger.error(e)
            response_data['state'] = "question not found"
        else:
            for canvasname, canvasitem in canvasmap.items():
                try:
                    if stdanswer:
                        canvas = Canvas.objects.get_or_create(name=str(canvasname),
                                                              question=question, stdanswer=stdanswer, stuanswer=None)
                    elif stuanswer:
                        canvas = Canvas.objects.get_or_create(name=str(canvasname),
                                                              question=question, stuanswer=stuanswer, stdanswer=None)
                    else:
                        canvas = Canvas.objects.get_or_create(name=str(canvasname),
                                                              question=question, stuanswer=None, stdanswer=None)
                except Exception, e:
                    logger.error(e)
                try:
                    canvas[0].axismap = pickle.dumps(canvasitem['axis'])
                    canvas[0].drawopts = pickle.dumps(canvasitem['drawopts'])
                    canvas[0].rulelist = pickle.dumps(canvasitem['rulelist'])
                except Exception, e:
                    logger.error(e)
                if stuanswer:
                    mark = __canvasmark(question, canvas[0])
                    canvas[0].mark = mark
                    response_data['canvasmark'] = mark
                canvas[0].save()
            response_data['state'] = "success"
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def __canvasmark(question, stucanvas):
    canvasname = stucanvas.name
    try:
        stdanswer = question.stdanswer
        stdcanvas = Canvas.objects.get(name=str(canvasname), question=question,
                                       stdanswer=stdanswer, stuanswer=None)
        stddrawopts = pickle.loads(str(stdcanvas.drawopts))
        stdrulelist = pickle.loads(str(stdcanvas.rulelist))
        stdpointlist = pickle.loads(str(stdcanvas.pointlist))
    except Exception, e:
        logger.error(e)
    else:
        canvascompare = Canvascompare()
        studrawopts = pickle.loads(str(stucanvas.drawopts))
        sturulelist = pickle.loads(str(stucanvas.rulelist))
        drawoptspair = canvascompare.comparecurvesimilarity(stddrawopts, studrawopts)
        logger.info(drawoptspair)
        correctlist = canvascompare.comparelist(sturulelist, stdrulelist)
        mark = canvascompare.mark(correctlist, stdpointlist)
        return mark


def canvas_get(request):
    if request.method == 'POST':
        response_data = {'state': 'failure'}
        try:
            canvasname = request.POST['name']
            id = json.loads(request.POST['id'].encode('utf-8'))
        except Exception, e:
            logger.error(e)
            response_data['state'] = "no name or id specified"
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
        try:
            question = Question.objects.get(id=id['questionid'])
            stdanswer = None
            stuanswer = None
            if id.get('stdanswerid'):
                stdanswer = question.stdanswer
            elif id.get('stuanswerid'):
                stuanswer = StudentAnswer.objects.get(id=id['stuanswerid'])
        except Exception, e:
            logger.error(e)
            response_data['state'] = "question not found"
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
        if stdanswer:
            try:
                canvas = Canvas.objects.get(name=canvasname, question=question,
                                            stdanswer=stdanswer, stuanswer=None)
            except:
                questioncanvas = Canvas.objects.get(name=canvasname, question=question,
                                                    stdanswer=None, stuanswer=None)
                canvas = Canvas.objects.create(name=canvasname, question=question,
                                               stdanswer=stdanswer, stuanswer=None,
                                               drawopts=questioncanvas.drawopts,
                                               axismap=questioncanvas.axismap,
                                               rulelist=questioncanvas.rulelist)
        elif stuanswer:
            try:
                canvas = Canvas.objects.get(name=canvasname, question=question,
                                            stuanswer=stuanswer, stdanswer=None)
                canvas.rulelist = pickle.dumps([])
                canvas.save()
            except Exception, e:
                logger.info(e)
                canvas = None
        else:
            try:
                canvas = Canvas.objects.get(name=canvasname, question=question,
                                            stdanswer=None, stuanswer=None)
            except Exception, e:
                logger.info(e)
                canvas = None
        if canvas:
            canvasmap = {canvasname: {'axis': pickle.loads(str(canvas.axismap)),
                                      'drawopts': pickle.loads(str(canvas.drawopts)),
                                      'rulelist': pickle.loads(str(canvas.rulelist))
                                      }
                         }
            if canvasmap:
                response_data['canvasmap'] = canvasmap
                response_data['state'] = 'success'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
