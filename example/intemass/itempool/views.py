import logging
from django.shortcuts import render_to_response
from django.template import RequestContext
from intemass.itempool.models import Itempool
from intemass.itempool.forms import ItemPoolDetailForm
from intemass.question.models import Question
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import get_object_or_404
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from portal.common import getTpByRequest

logger = logging.getLogger(__name__)


def __getItempool(itempoolid, tp=None):
    if not itempoolid or itempoolid == "-1":
        if tp:
            return Itempool.objects.create(teacher=tp)
        else:
            return None
    return get_object_or_404(Itempool, id=int(itempoolid))


@permission_required('auth.add_user')
def itempool_add(request):
    tp, res = getTpByRequest(request, "login")
    if not tp and res:
        return res
    if request.method == "POST":
        form = ItemPoolDetailForm(request.POST, teacher=tp)
        if form.is_valid():
            pass
    else:
        itempoolid = request.GET.get('itempoolid')
        try:
            i = Itempool.objects.get(id=itempoolid)
        except:
            form = ItemPoolDetailForm(teacher=tp)
        else:
            form = ItemPoolDetailForm(teacher=tp,
                                      initial={'itempoolid': i.id,
                                               'itempoolname': i.poolname})
    logger.info("itempool all...")
    return render_to_response('itempool_detail.html', {'form': form},
                              context_instance=RequestContext(request))


@permission_required('auth.add_user')
def itempool_getall(request):
    logger.info("itempool getall...")
    tp, res = getTpByRequest(request, "login")
    if not tp and res:
        return res
    itempools = []
    if tp:
        try:
            itempools = Itempool.objects.filter(teacher=tp)
        except:
            pass
    response = render_to_response('itempool_all.json',
                                  {'itempools': itempools},
                                  context_instance=RequestContext(request))
    response['Content-Type'] = 'text/plain; charset=utf-8'
    response['Cache-Control'] = 'no-cache'
    return response


@permission_required('auth.add_user')
def itempool_getquestions(request):
    logger.info("getstudents...")
    tp, res = getTpByRequest(request, None)
    questions = []
    view = 0
    if tp:
        itempoolid = request.GET.get("itempoolid")
        view = request.GET.get("view")
        logger.info("itempoolid:%s" % itempoolid)
        if itempoolid:
            try:
                itempool = Itempool.objects.get(id=int(itempoolid))
            except:
                itempool = None
            else:
                logger.info("itempool:%s" % itempool)
                try:
                    questions = Question.objects.filter(teacher=tp, itempool=itempool)
                except:
                    logger.info("no questions in %s" % itempool)
    if view:
        response = render_to_response('itempool_allquestions_readonly.json',
                                      {'questions': questions},
                                      context_instance=RequestContext(request))
    else:
        response = render_to_response('itempool_allquestions.json',
                                      {'questions': questions},
                                      context_instance=RequestContext(request))
    response['Content-Type'] = 'text/plain; charset=utf-8'
    response['Cache-Control'] = 'no-cache'
    return response


@permission_required('auth.add_user')
def itempool_updatename(request):
    logger.info("itempool_updatename...")
    tp, res = getTpByRequest(request, None)
    response_data = {'state': 'failure'}
    if tp:
        itempoolid = request.GET.get("itempoolid").strip()
        itempoolname = request.GET.get("itempoolname").strip()
        logger.info("itempoolid:%s,name:%s" % (itempoolid, itempoolname))
        if itempoolid and itempoolname:
            itempool = __getItempool(itempoolid, tp)
            logger.info(" get itempool %s" % itempool)
            if itempool:
                itempool.poolname = itempoolname
                itempool.save()
                response_data['itempoolid'] = itempool.id
                response_data['itempoolname'] = itempool.poolname
                response_data['state'] = 'success'
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")


class ItempoolDelete(DeleteView):
    success_url = reverse_lazy("deleteview_callback")
    model = Itempool

    def get_object(self):
        pk = self.request.POST['itempoolid']
        return get_object_or_404(Itempool, id=pk)


def itempool_updatedesc(request):
    tp, res = getTpByRequest(request, None)
    response_data = {"state": "failure"}
    if request.method == 'POST':
        if tp:
            itempoolid = request.POST.get("itempoolid").strip()
            description = request.POST.get("description").replace('\r', '').replace('\n', '</br>').strip()
            logger.info("itempoolid:%s,desc:%s" % (itempoolid, description))
            if itempoolid:
                itempool = __getItempool(itempoolid, tp)
                logger.info(" get itempool %s" % itempool)
                if itempool:
                    itempool.description = description
                    itempool.save()
                    response_data['description'] = itempool.description.replace('</br>', '\n')
                    response_data['state'] = "success"
    else:
        itempoolid = request.GET.get("itempoolid").strip()
        if itempoolid and itempoolid != '-1':
            itempool = __getItempool(itempoolid, tp)
            response_data['description'] = itempool.description.replace('</br>', '\n')
            response_data['state'] = "success"
    return HttpResponse(simplejson.dumps(response_data), mimetype="application/json")
