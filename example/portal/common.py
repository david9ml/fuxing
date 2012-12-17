import logging
from django.shortcuts import redirect
from django.contrib import messages
from intemass.portal.models import TProfile, SProfile
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def getGroupNameByRequest(request):
    groups = request.user.groups.all()
    if groups and len(groups) > 0:
        return groups[0].name
    else:
        return None


def getTpByRequest(request, redirectUrl):
    group = getGroupNameByRequest(request)
    if group == "teachers":
        try:
            tp = TProfile.objects.get(user=request.user)
        except:
            messages.add_message(request, messages.SUCCESS, "No this user" % request.user.username)
            if redirectUrl:
                return None, redirect(redirectUrl)
            else:
                return None, None
    else:
        if redirectUrl:
            messages.add_message(request, messages.SUCCESS, "You(%s) are not tearchers" % request.user.username)
            res = redirect(redirectUrl)
            return None, res
        else:
            return None, None
    return tp, None


def getSpByRequest(request, redirectUrl):
    group = getGroupNameByRequest(request)
    if group == "students":
        try:
            sp = SProfile.objects.get(user=request.user)
        except:
            messages.add_message(request, messages.SUCCESS, "No this user" % request.user.username)
            if redirectUrl:
                return None, redirect(redirectUrl)
            else:
                return None, None
    else:
        if redirectUrl:
            messages.add_message(request, messages.SUCCESS, "You(%s) are not students" % request.user.username)
            res = redirect(redirectUrl)
            return None, res
        else:
            return None, None
    return sp, None


def getSpById(sp_id):
    try:
        sp = SProfile.objects.get(user=User.objects.get(id=sp_id))
    except:
        sp = None
        logger.info("sprofile not found:%s" % sp_id)
        pass
    return sp


def getTpById(tp_id):
    try:
        tp = TProfile.objects.get(user=User.objects.get(id=tp_id))
    except:
        tp = None
        logger.info("tprofile not found:%s" % tp_id)
        pass
    return tp


def stripHTMLStrings(html):
    """
        Strip HTML tags from any string and transfrom special entities
    """
    text = html

    # replace special strings
    special = {'&nbsp;': ' ', '&amp;': '&', '&quot;': '"',
               '&lt;': '<', '&gt;': '>', '&ldquo;': '"',
               '&rdquo;': '"', '&hellip;': '...'}

    for (k, v) in special.items():
        text = text.replace(k, v)
    return text
