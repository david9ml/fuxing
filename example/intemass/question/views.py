import os
import sys
import re
import Image
import pickle
import logging
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json
from django.conf import settings
from django.utils.html import strip_tags
from intemass.question.models import Question, QuestionImage, StandardAnswer
from intemass.student.models import StudentAnswer
from intemass.itempool.models import Itempool
from portal.common import getTpByRequest, getSpByRequest, stripHTMLStrings
from portal.models import SProfile
from canvas.models import Canvas
from algo.standard import Standard
from algo.markscheme import MarkScheme
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import DeleteView
from intemass.paper.models import Paper
import hashlib

logger = logging.getLogger(__name__)


@permission_required('auth.add_user')
def question_add(request):
    tp, res = getTpByRequest(request, 'login')
    if not tp and res:
        return res
    questionid = request.GET.get('questionid')
    selitempoolid = request.GET.get('itempoolid')
    logger.info("sel itempool id:%s, question id:%s" % (selitempoolid, questionid))
    try:
        itempools = Itempool.objects.filter(teacher=tp)
    except:
        itempools = []
    try:
        questions = Question.objects.filter(teacher=tp)
    except:
        questions = []
    return render_to_response('question_detail.html',
                              {'selitempoolid': selitempoolid,
                               'questionid': questionid,
                               'itempools': itempools,
                               'questions': questions},
                              context_instance=RequestContext(request))


@permission_required('auth.add_user')
def question_updatename(request):
    logger.info("question_updatename...")
    tp, res = getTpByRequest(request, None)
    response_data = {"state": "failure"}
    if tp and request.method == 'POST':
        questionid = request.POST.get("questionid")
        questionname = request.POST.get("questionname")
        itempoolid = request.POST.get("itempoolid")
        try:
            itempool = Itempool.objects.get(id=int(itempoolid))
        except:
            itempool = None
        if questionid and questionname and itempool:
            logger.info("questionid:%s,name:%s" % (questionid, questionname))
            if questionid == "-1":
                question = Question.objects.create(teacher=tp,
                                                   qname=questionname.strip(),
                                                   itempool=itempool)
            else:
                question = Question.objects.get(id=int(questionid.strip()))
                question.qname = questionname.strip()
                question.save()
            logger.info("question %s" % question)
            response_data['questionid'] = question.id
            response_data['questiontype'] = question.qtype
            response_data['description'] = question.description
            response_data['state'] = "success"
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def __pointanalysis(fulltext):
    pointlist = []
    text = fulltext.replace('\t', '')
    p = re.compile(r'^\d[\d\D]+?\n$', re.M)
    m = p.findall(text)
    logger.info(m)
    for i in range(0, len(m)):
        num = re.search(r'\d(\.\d)*', m[i]).group()
        pointlist.append({'Point_No': 'P' + num,
                          'Point_Text': m[i][len(num):].replace('\n', ' ')})
    return pointlist


def __changeNameForStd(name, qid):
    nameArr = re.split('\.', name)
    if len(nameArr) < 2:
        return None, None
    else:
        imagename = "std__%s__%s.%s" % ("_".join(nameArr[:-1]), qid, nameArr[-1])
        thumbname = "thumb__std__%s__%s.%s" % ("_".join(nameArr[:-1]), qid, nameArr[-1])
        return imagename, thumbname


def __changeName(name, qid):
    nameArr = re.split('\.', name)
    if len(nameArr) < 2:
        return None, None
    else:
        imagename = "%s__%s.%s" % ("_".join(nameArr[:-1]), qid, nameArr[-1])
        thumbname = "thumb__%s__%s.%s" % ("_".join(nameArr[:-1]), qid, nameArr[-1])
        return imagename, thumbname


def __saveImage(image, fpath, fname):
    m = hashlib.md5()
    fullname = os.path.join(fpath, fname)
    with open(fullname, 'wb+') as destination:
        for chunk in image.chunks():
            m.update(chunk)
            destination.write(chunk)
    logger.info('md5')
    return fullname, m.hexdigest()


def __resizeImage(imageIn, imageOut):
    orig = Image.open(imageIn)
    origW, origH = orig.size
    destW = 75
    rate = float(destW) / float(origW)
    destH = origH * rate
    try:
        orig.thumbnail((destW, destH))
        orig.save(imageOut)
    except:
        logger.error("resize image failed")


@csrf_exempt
def questionimage_upload(request):
    if request.method == 'POST':
        questionid = request.POST["questionid"]
        isStandardImage = request.POST.get('standard_image')
        image = request.FILES.get('Filedata', None)
        try:
            question = Question.objects.get(id=questionid)
        except:
            logger.info('question not exists')
            logger.error(sys.exc_info())
            return HttpResponse("Upload Error")
        else:
            if isStandardImage and isStandardImage == 'yes':
                iscorrect = True
                imagename, thumbname = __changeNameForStd(image.name, questionid)
                questionimages = QuestionImage.objects.filter(question=question).exclude(description='del')
                digests = list(questionimage.digest for questionimage in questionimages)
                uploadeddigestimages = QuestionImage.objects.filter(question=question,
                                                                    iscorrect=True).exclude(description='del')
                stddigests = list(i.digest for i in uploadeddigestimages)
                uploadImageFullName, digest = __saveImage(image, settings.UPLOADFOLDER, imagename)
                if digest in digests and digest not in stddigests:
                    description = None
                else:
                    description = 'del'
            else:
                iscorrect = False
                imagename, thumbname = __changeName(image.name, questionid)
                uploadImageFullName, digest = __saveImage(image, settings.UPLOADFOLDER, imagename)
                #in case uploaded the same img
                questionimages = QuestionImage.objects.filter(question=question).exclude(description='del')
                digests = list(questionimage.digest for questionimage in questionimages)
                if digest in digests:
                    description = 'del'
                else:
                    description = None

            __resizeImage(uploadImageFullName,
                          os.path.join(settings.THUMBNAILFOLDER, thumbname))
            logger.info("Image Name:%s,Image Thumbnail Name:%s" % (imagename, thumbname))
        try:
            imageObj = QuestionImage.objects.create(question=question,
                                                    imagename=image.name,
                                                    abspath=imagename,
                                                    digest=digest,
                                                    description=description,
                                                    iscorrect=iscorrect)
            imageObj.save()
        except:
            print sys.exc_info()
            return HttpResponse("Upload Error")
        logger.info("upload sucessful")
        return HttpResponse("Upload Success!", mimetype="text/plain")
    else:
        return HttpResponse("Upload Error!", mimetype="text/plain")


@permission_required('auth.add_user')
def question_deleteimage(request):
    response_data = {'state': 'failure'}
    if request.method == 'POST':
        imageid = request.POST["imageid"]
        try:
            imageToDelete = QuestionImage.objects.get(id=imageid)
        except:
            pass
        else:
            imageToDelete.description = 'del'
            imageToDelete.save()
            response_data['state'] = 'success'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


@permission_required('auth.add_user')
def question_submit(request):
    response_data = {'state': 'failure'}
    tp, res = getTpByRequest(request, None)
    questionid = int(request.POST['questionid'])
    itempoolid = int(request.POST.get('itempoolid'))
    question_content = request.POST['question_content']
    canvasname = request.POST['canvasname']
    logger.info("qid:%d, iid:%d" % (questionid, itempoolid))
    try:
        itempool = Itempool.objects.get(teacher=tp, id=itempoolid)
        question = Question.objects.get(id=questionid)
    except:
        itempool = None
        question = None
    else:
        _updatecanvas(question, canvasname)
        logger.info("itempool:%s" % itempool)
        logger.info("question:%s" % question)
        if not question_content:
            question.infocompleted &= ~Question.QUESTIONCOMPLETED
            question.save()
        else:
            logger.info("content:%s" % question_content)
            question.qname = request.POST['question_name']
            question.description = request.POST['question_desc']
            question.qtype = request.POST['question_type']
            logger.info("qname:%s, desc:%s, qtype:%s" % (question.qname, question.description, question.qtype))
            question.itempool = itempool
            question.teacher = tp
            question.qhtml = question_content
            question.qtext = stripHTMLStrings(strip_tags(question_content))
            question.infocompleted |= Question.QUESTIONCOMPLETED
            question.save()
            logger.info(question.infocompleted)
            if question.infocompleted == Question.ALLCOMPLETED:
                _updatepaper(question)
            logger.info(question.infocompleted)
            response_data['state'] = 'success'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def _updatecanvas(question, canvasinfo, stdanswer=None):
    if not canvasinfo:
        return None
    try:
        canvasname = [cname.strip('"') for cname in canvasinfo.strip('[]').split(',')]
        canvaslist = Canvas.objects.filter(question=question, stdanswer=stdanswer)
        delcanvaslist = canvaslist.exclude(name__in=canvasname)
        logger.debug(delcanvaslist)
        for canvas in delcanvaslist:
            canvas.delete()
    except Exception, e:
        logger.error(e)
    else:
        retcanvas = {}
        for canvas in canvaslist:
            if canvas.name in canvasname:
                try:
                    rulelist = pickle.loads(str(canvas.rulelist))
                except:
                    rulelist = []
                try:
                    markscheme = pickle.loads(str(canvas.markscheme))
                except:
                    markscheme = {}
                try:
                    pointlist = pickle.loads(str(canvas.pointlist))
                except:
                    pointlist = {}
                retcanvas[canvas.name] = {'id': canvas.id, 'occur': 1,
                                          'rulelist': rulelist,
                                          'markscheme': markscheme,
                                          'pointlist': pointlist}
        return retcanvas


@permission_required('auth.add_user')
def question_get(request):
    logger.info("question get")
    tp, res = getTpByRequest(request, None)
    response_data = {'state': 'failure'}
    if tp and request.method == 'POST':
        questionid = request.POST.get("questionid")
        logger.info("questionid:%s" % questionid)
        if questionid and questionid != '-1':
            question = Question.objects.get(id=int(questionid))
            logger.info("question %s" % question)
            questioncanvas, stdanswercanvas = __getcanvas(question)
            response_data['question_desc'] = question.description
            response_data['question_type'] = question.qtype
            response_data['question_content'] = question.qhtml
            response_data['standard_content'] = question.stdanswerhtml
            response_data['question_item'] = question.itempool.id
            response_data['question_canvas'] = questioncanvas
            response_data['stdanswer_canvas'] = stdanswercanvas
            rawArr = question.markscheme.split(',')
            if rawArr:
                schemelist = []
                if len(rawArr) >= 2:
                    for i in range(0, len(rawArr), 2):
                        str1 = str(rawArr[i])
                        str2 = str(rawArr[i + 1])
                        schemelist.append([str1, str2])
                response_data['question_markscheme'] = schemelist
            try:
                rulelist = pickle.loads(str(question.stdanswer.rulelist))
            except:
                rulelist = []
            try:
                imgrulelist = pickle.loads(str(question.stdanswer.imgrulelist))
            except:
                imgrulelist = []

            canvasrulelistlen = 0
            for canvasname in stdanswercanvas:
                canvasrulelistlen += len(stdanswercanvas[canvasname]['pointlist'])
            response_data['rulecount'] = len(rulelist) + len(imgrulelist) + canvasrulelistlen
            response_data['rulelist'] = (rulelist + imgrulelist)[:5000]
            response_data['state'] = 'success'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def __getcanvas(question):
    try:
        stdanswer = question.stdanswer
        questioncanvaslist = Canvas.objects.filter(question=question,
                                                   stdanswer=None, stuanswer=None)
        stdanswercanvaslist = Canvas.objects.filter(question=question,
                                                    stdanswer=stdanswer, stuanswer=None)
    except:
        return None, None
    else:
        questioncanvas = {}
        for canvas in questioncanvaslist:
            questioncanvas[canvas.name] = {'id': canvas.id, 'occur': 1}
        stdanswercanvas = {}
        for canvas in stdanswercanvaslist:
            try:
                rulelist = pickle.loads(str(canvas.rulelist))
            except:
                rulelist = []
            try:
                markscheme = pickle.loads(str(canvas.markscheme))
            except:
                markscheme = {}
            try:
                pointlist = pickle.loads(str(canvas.pointlist))
            except:
                pointlist = {}
            stdanswercanvas[canvas.name] = {'id': canvas.id, 'occur': 1,
                                            'rulelist': rulelist, 'pointlist': pointlist,
                                            'markscheme': markscheme}
        return questioncanvas, stdanswercanvas


@login_required
def stu_question_get(request):
    logger.info("question get")
    student, res = getSpByRequest(request, None)
    response_data = {'state': 'failure'}
    if request.method == 'POST':
        questionid = request.POST.get("questionid")
        logger.info("questionid:%s" % questionid)
        if questionid and questionid != '-1':
            question = Question.objects.get(id=int(questionid))
            logger.info("question %s" % question)
            response_data['question_desc'] = question.description
            response_data['question_content'] = question.qhtml
            try:
                stuanswer = StudentAnswer.objects.get(question=question, student=student)
                html_answer = stuanswer.html_answer
            except Exception, e:
                logger.error(e)
                pass
            else:
                response_data['question_canvas'] = __getstucanvas(question, stuanswer)
                response_data['question_stuanswer'] = html_answer
                response_data['stuanswerid'] = stuanswer.id
                response_data['state'] = 'success'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def __getstucanvas(question, stuanswer):
    try:
        question_canvas = Canvas.objects.filter(question=question,
                                                stdanswer=None, stuanswer=None)
    except:
        return []
    else:
        stuanswer_canvaslist = []
        for canvas in question_canvas:
            try:
                stuanswer_canvas = Canvas.objects.get(question=question, name=canvas.name, stuanswer=stuanswer)
            except Exception, e:
                logger.error(e)
                stuanswer_canvas = Canvas.objects.create(name=canvas.name, question=question, stuanswer=stuanswer)
            if stuanswer_canvas.drawopts is None and stuanswer_canvas.axismap is None:
                stuanswer_canvas.axismap = canvas.axismap
                stuanswer_canvas.drawopts = canvas.drawopts
                stuanswer_canvas.rulelist = pickle.dumps({})
                stuanswer_canvas.save()
            stuanswer_canvaslist.append(stuanswer_canvas.name)
        return stuanswer_canvaslist


@login_required
def stu_question_thumbnails(request):
    logger.info("student question thumbnails")
    response_data = {'state': 'failure'}
    student, res = getSpByRequest(request, None)
    if request.method == 'POST':
        questionid = request.POST.get("questionid")
        iscorrectParam = request.POST.get("iscorrect")
        if iscorrectParam and iscorrectParam == 'yes':
            iscorrect = True
        else:
            iscorrect = False
        logger.info("questionid:%s iscorrect:%s" % (questionid, iscorrect))
        if questionid and questionid != '-1':
            try:
                question = Question.objects.get(id=int(questionid))
                studentanswer = StudentAnswer.objects.get(question=question,
                                                          student=student)
            except:
                studentanswer = None
                thumbnails = QuestionImage.objects.filter(question=question,
                                                          iscorrect=False)\
                    .exclude(description="del")
                stuthumbnails = None
            else:
                stuthumbnails = studentanswer.stuansimages.all()
                studigests = list(st.digest for st in stuthumbnails)
                thumbnails = QuestionImage.objects.filter(question=question,
                                                          iscorrect=False)\
                    .exclude(description="del")\
                    .exclude(digest__in=studigests)
            logger.info("question %s, thumbnails%s" % (question, thumbnails))
                #[0] thumb,[1] imagename,[2] orig image
            if thumbnails:
                response_data['thumbnails'] = list(["%s/thumb__%s" % (settings.THUMBNAILPREFIX, t.abspath),
                                                    t.imagename,
                                                    "%s/%s" % (settings.UPLOADPREFIX, t.abspath),
                                                    t.id] for t in thumbnails)
            if stuthumbnails:
                response_data['stuthumbnails'] = list(["%s/thumb__%s" % (settings.THUMBNAILPREFIX, t.abspath),
                                                      t.imagename,
                                                      "%s/%s" % (settings.UPLOADPREFIX, t.abspath),
                                                      t.id] for t in stuthumbnails)
            response_data['state'] = 'success'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


@permission_required('auth.add_user')
def question_thumbnails(request):
    logger.info("question thumbnails")
    tp, res = getTpByRequest(request, None)
    response_data = {'state': 'failure'}
    if tp and request.method == 'POST':
        iscorrectParam = request.POST.get("iscorrect")
        if iscorrectParam and iscorrectParam == 'yes':
            iscorrect = True
        else:
            iscorrect = False
        try:
            questionid = request.POST.get("questionid")
            if questionid and questionid != '-1':
                question = Question.objects.get(id=int(questionid))
                thumbnails = QuestionImage.objects.filter(question=question, iscorrect=iscorrect).exclude(description='del')
            else:
                thumbnails = []
        except Exception, e:
            logger.error(e)
        if thumbnails:
            if iscorrect:
                questionimglist = pickle.loads(str(question.imagepointlist))
                logger.info(questionimglist)
                stdthumbnails = list([imagepoint, t]
                                     for imagepoint in questionimglist
                                     for t in thumbnails
                                     if imagepoint['Point_Text'] is t.digest)
                logger.info(stdthumbnails)
                response_data['thumbnails'] = list(["%s/thumb__%s" % (settings.THUMBNAILPREFIX, t.abspath),
                                                   i['Point_No'],
                                                   "%s/%s" % (settings.UPLOADPREFIX, t.abspath),
                                                   t.id] for i, t in stdthumbnails)
                response_data['stdthumbnail_ids'] = list(t.id for t in thumbnails)
            else:
                pointlist = list({'Point_No': u'P0.' + str(i + 1),
                                  'Point_Text': image.digest}
                                 for i, image in enumerate(thumbnails))
                question.imagepointlist = pickle.dumps(pointlist)
                question.save()
                response_data['thumbnails'] = list(["%s/thumb__%s" % (settings.THUMBNAILPREFIX, t.abspath),
                                                    ("P0.%s" % str(i + 1)),
                                                    "%s/%s" % (settings.UPLOADPREFIX, t.abspath),
                                                    t.id] for i, t in enumerate(thumbnails))
            response_data['state'] = 'success'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


@permission_required('auth.add_user')
def question_submitstandard(request):
    response_data = {'state': 'failure'}
    questionid = int(request.POST['questionid'])
    canvasname = request.POST['canvasname']
    logger.info("qid:%d" % questionid)
    try:
        question = Question.objects.get(id=questionid)
    except:
        logger.error('No question found')
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    logger.info("question:%s" % question)
    try:
        txtstdanswer = {'html': request.POST['standard_content']}
        txtstdanswer['text'] = stripHTMLStrings(strip_tags(txtstdanswer['html']))
    except Exception, e:
        logger.error(e)
    else:
        logger.debug("content:%s" % txtstdanswer)

    stdanswer = __parsestdanswer(question, txtstdanswer)
    stdanswer_canvas = _updatecanvas(question, canvasname, stdanswer)
    logger.debug(stdanswer_canvas)
    questioncomplete = __updatestdanswer(question, stdanswer, txtstdanswer)
    if questioncomplete:
        _updatepaper(question)
    logger.info(question.infocompleted)
    response_data['stdanswer_canvas'] = stdanswer_canvas
    response_data['state'] = 'success'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def __parsestdanswer(question, txtstdanswer):
    if not txtstdanswer['text']:
        return None
    #parse txtpointlist
    sinst = Standard()
    pointlist, textfdist, slist = sinst.Analysis(txtstdanswer['text'])
    #parse imagepointlist
    try:
        imagepointlist = pickle.loads(str(question.imagepointlist))
    except:
        pass
    else:
        for imagepoint in imagepointlist:
            pointlist.append(imagepoint)

    logger.debug(pointlist)
    pnlist = list(point['Point_No'] for point in pointlist)
    if pnlist:
        textfdist_dumpped = pickle.dumps(textfdist)
        sentencelist_dumpped = pickle.dumps(slist)
        pointlist_dumpped = pickle.dumps(pointlist)
        try:
            stdanswer, created = StandardAnswer.objects.get_or_create(name=question.qname,
                                                                      textfdist=textfdist_dumpped,
                                                                      sentencelist=sentencelist_dumpped,
                                                                      pointlist=pointlist_dumpped)
        except Exception, e:
            logger.error(e)
            stdanswer = None
        else:
            logger.info(stdanswer)
    else:
        stdanswer = None
    return stdanswer


def __updatestdanswer(question, stdanswer, txtanswer):
    if stdanswer:
        question.stdanswertext = txtanswer['text']
        question.stdanswerhtml = txtanswer['html']
        question.stdanswer = stdanswer
        question.infocompleted |= Question.STDANSWERCOMPLETED
    else:
        question.infocompleted &= ~Question.STDANSWERCOMPLETED
    question.save()
    return (question.infocompleted == Question.ALLCOMPLETED)


@permission_required('auth.add_user')
def question_submitmark(request):
    tp, res = getTpByRequest(request, None)
    response_data = {'state': 'failure'}
    try:
        questionid = request.POST['questionid']
        question = Question.objects.get(id=questionid)
        stdanswer = question.stdanswer
    except:
        question = None
        stdanswer = None
    else:
        logger.info("question:%s" % question)
        rawschemes = request.POST['schemes']
        scheme = __parsescheme(rawschemes)
        rulecount, rulelist = __updaterulelist(scheme, stdanswer)

        #update canvas rules
        rawcanvasschemes = request.POST['canvasschemes']
        canvasscheme = __parsecanvasscheme(rawcanvasschemes)
        canvasrulecount, canvasrulelist = __updatecanvasmarkscheme(canvasscheme, question, stdanswer)

        questioncomplete = __updatesheme(question, stdanswer, rawschemes)
        if questioncomplete:
            _updatepaper(question)

        response_data['canvasrulelist'] = canvasrulelist
        response_data['rulelist'] = rulelist
        response_data['rulecount'] = rulecount + canvasrulecount
        if rulelist:
            response_data['state'] = 'success'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def __parsescheme(rawschemes):
    rawschemelist = rawschemes.split(',')
    imgschemelist = []
    txtschemelist = []
    if len(rawschemelist) >= 2:
        for i in range(0, len(rawschemelist), 2):
            str1 = str(rawschemelist[i])
            str2 = str(rawschemelist[i + 1])
            if 'P0.' in str1:
                imgschemelist.append([str1, str2])
            else:
                txtschemelist.append([str1, str2])
    txtschemelist.sort(key=lambda x: int(x[1]), reverse=True)
    imgschemelist.sort(key=lambda x: int(x[1]), reverse=True)
    if txtschemelist and imgschemelist:
        fullmark = int(imgschemelist[0][1]) + int(txtschemelist[0][1])
    else:
        fullmark = int(txtschemelist[0][1])
    return {'txtscheme': txtschemelist, 'imgscheme': imgschemelist, 'fullmark': fullmark}


def __updaterulelist(scheme, stdanswer):
    if not stdanswer:
        return 0, None
    try:
        std_pointlist = pickle.loads(str(stdanswer.pointlist))
    except:
        stdanswer = None
        count = 0
        nestedrulelist = []
    else:
        #rulelist
        txtplist = list(point['Point_No'] for point in std_pointlist if 'P0.' not in point['Point_No'])
        txtrulelist = []
        if txtplist:
            try:
                ms = MarkScheme(txtplist)
                txtrulelist = list(rule for rule in ms.GetRules(scheme['txtscheme']))
            except:
                pass

        #imgrulelist
        imgplist = list(point['Point_No'] for point in std_pointlist if 'P0.' in point['Point_No'])
        imgrulelist = []
        if imgplist:
            try:
                ms = MarkScheme(imgplist)
                imgrulelist = list(rule for rule in ms.GetRules(scheme['imgscheme']))
            except:
                pass

        try:
            stdanswer.rulelist = pickle.dumps(txtrulelist)
            stdanswer.imgrulelist = pickle.dumps(imgrulelist)
            stdanswer.fullmark = scheme['fullmark']
            stdanswer.save()
        except Exception, e:
            logger.error(e)
            count = 0
            nestedrulelist = []
        else:
            rulelist = txtrulelist + imgrulelist
            count = len(rulelist)
            nestedrulelist = rulelist[:5000]
    return count, nestedrulelist


def __parsecanvasscheme(rawschemes):
    rawschemelist = rawschemes.split(',')
    schemelist = {}
    if len(rawschemelist) >= 2:
        for i in range(0, len(rawschemelist), 2):
            [canvasname, scheme] = str(rawschemelist[i]).split(':')
            schemelist.setdefault(canvasname, [])
            mark = str(rawschemelist[i + 1])
            schemelist[canvasname].append([scheme, mark])
        return schemelist
    else:
        return None


def __updatecanvasmarkscheme(scheme, question, stdanswer):
    if not scheme:
        return 0, None
    totalcanvasrulelist = []
    for canvasname in scheme:
        canvasscheme = scheme[canvasname]
        try:
            stdcanvas = Canvas.objects.get(name=canvasname, question=question, stdanswer=stdanswer)
            stdcanvasplist = list(rule[0] for rule in pickle.loads(str(stdcanvas.rulelist)))
        except Exception, e:
            logger.error(e)
        else:
            try:
                logger.debug(stdcanvasplist)
                logger.debug(canvasscheme)
                ms = MarkScheme(stdcanvasplist)
                canvasrulelist = list(rule for rule in ms.GetRules(canvasscheme))
                stdcanvas.pointlist = pickle.dumps(canvasrulelist)
                stdcanvas.markscheme = pickle.dumps(canvasscheme)
                stdcanvas.save()
            except Exception, e:
                logger.error(e)
                stdcanvas.markscheme = None
            else:
                for canvasrule in canvasrulelist:
                    canvasrule['Name'] = canvasname
                totalcanvasrulelist += canvasrulelist
    return len(totalcanvasrulelist), totalcanvasrulelist


def __updatesheme(question, stdanswer, rawschemes):
    if stdanswer:
        try:
            question.stdanswer = stdanswer
            question.markscheme = rawschemes
            question.infocompleted |= Question.MARKSCHEMECOMPLETED
            question.save()
        except Exception, e:
            logger.error(e)
            pass
        else:
            return (question.infocompleted == Question.ALLCOMPLETED)
    question.infocompleted &= ~Question.MARKSCHEMECOMPLETED
    question.save()
    return False


def _updatepaper(question):
    if question and question.infocompleted is Question.ALLCOMPLETED:
        papers = question.paper.all()
        for p in papers:
            questions = Question.objects.filter(paper=p, infocompleted=Question.ALLCOMPLETED)
            p.total = len(questions)
            p.save()


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy("deleteview_callback")

    def get_object(self):
        pk = self.request.POST['questionid']
        return get_object_or_404(Question, id=pk)


@login_required
def question_getpointmarklist(request):
    student, res = getSpByRequest(request, None)
    questionid = request.POST.get('questionid')
    try:
        question = Question.objects.get(id=questionid)
        studentanswer = StandardAnswer.objects.get(student=student, question=question)
    except:
        return HttpResponse('cant find the specified answer')
    answerdetail = {'mark': studentanswer.mark}
    p = re.compile('\'(.*?)\'')
    answerdetail['pointmarklist'] = p.findall(studentanswer.pointmarklist)
    p = re.compile('\[\'(.*?)\'')
    omittedpoint = p.findall(studentanswer.omitted)
    omittedlist = list('P'.join(o) for o in omittedpoint)
    answerdetail['omittedlist'] = omittedlist
    return HttpResponse(json.dumps(answerdetail), mimetype="application/json")


@login_required
def question_getstdanswer(request):
    logger.info("stdanswer get")
    response_data = {'state': 'failure'}
    if request.method == 'POST':
        questionid = request.POST.get("questionid")
        logger.info("questionid:%s" % questionid)
        if questionid and questionid != '-1':
            question = Question.objects.get(id=int(questionid))
            logger.info("question %s" % question)
            response_data['answer_content'] = question.stdanswerhtml
            response_data['state'] = 'success'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


@login_required
def questionid_get(request):
    logger.info("question id get")
    response_data = {'state': 'failure'}
    if request.method == 'POST':
        paperid = request.POST.get("paperid")
        logger.info(paperid)
        if paperid:
            try:
                paper = Paper.objects.get(id=paperid)
                qids = pickle.loads(str(paper.questionseq))
                qnames = list(Question.objects.get(id=qid).qname for qid in qids)
            except Exception, e:
                logger.error(e)
            else:
                response_data['qids'] = qids
                response_data['qnames'] = qnames
                response_data['state'] = 'success'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


@login_required
def question_getstureport(request):
    response_data = {'state': 'failure'}
    stuid = request.POST.get('studentid')
    qid = request.POST.get('questionid')
    try:
        question = Question.objects.get(id=qid)
        stdanswer = question.stdanswer
        stdcanvaslist = Canvas.objects.filter(question=question, stdanswer=stdanswer, stuanswer=None)
        student = SProfile.objects.get(user__id=stuid)
        stuanswer = StudentAnswer.objects.get(question=question, student=student)
        stucanvaslist = Canvas.objects.filter(question=question, stuanswer=stuanswer, stdanswer=None)
    except Exception, e:
        logger.error(e)
    else:
        response_data['canvas'] = {'stucanvas': [[stuanswer.id, stucanvas.name] for stucanvas in stucanvaslist],
                                   'stdcanvas': [[stdanswer.id, stdcanvas.name] for stdcanvas in stdcanvaslist]
                                   }
        response_data['stuname'] = student.user.username
        response_data['mark'] = stuanswer.mark
        response_data['question'] = question.qhtml
        response_data['stuanswer'] = stuanswer.html_answer
        response_data['pointmarklist'] = stuanswer.pointmarklist
        if stuanswer.omitted:
            omitted = pickle.loads(str(stuanswer.omitted))
            response_data['omitted'] = omitted
            logger.info("omitted: %s" % omitted)
        else:
            response_data['omitted'] = ''
        response_data['state'] = 'success'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


@login_required
def report_thumbnails(request):
    response_data = {'state': 'failure'}
    logger.info("report question thumbnails")
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        if studentid:
            try:
                student = SProfile.objects.get(user__id=studentid)
            except:
                student, res = getSpByRequest(request, None)
        questionid = request.POST.get("questionid")
        if questionid and questionid != '-1':
            try:
                question = Question.objects.get(id=int(questionid))
                stuanswer = StudentAnswer.objects.get(question=question, student=student)
            except:
                question = None
                stuanswer = None
            else:
                response_data = __getreportthumbnails(question, stuanswer)
    return HttpResponse(json.dumps(response_data), mimetype="application/json")


def __getreportthumbnails(question, stuanswer):
    logger.info("question %s,stuanswer%s" % (question, stuanswer))
    response_data = {'state': 'failure'}
    try:
        questionthumbnails = QuestionImage.objects.filter(question=question).exclude(description="del")
        stdthumbnails = QuestionImage.objects.filter(question=question, iscorrect=True).exclude(description="del")
        stuthumbnails = stuanswer.stuansimages.all()
    except:
        pass
    else:
        response_data['questionthumbnails'] = list(["%s/thumb__%s" % (settings.THUMBNAILPREFIX, t.abspath),
                                                    t.imagename,
                                                    "%s/%s" % (settings.UPLOADPREFIX, t.abspath),
                                                    t.id]
                                                   for t in questionthumbnails)
        response_data['stuthumbnails'] = list(["%s/thumb__%s" % (settings.THUMBNAILPREFIX, t.abspath),
                                               t.imagename,
                                               "%s/%s" % (settings.UPLOADPREFIX, t.abspath),
                                               t.id]
                                              for t in stuthumbnails)
        response_data['stdthumbnails'] = list(["%s/thumb__%s" % (settings.THUMBNAILPREFIX, t.abspath),
                                               t.imagename,
                                               "%s/%s" % (settings.UPLOADPREFIX, t.abspath),
                                               t.id]
                                              for t in stdthumbnails)
        response_data['state'] = 'success'
    return response_data
