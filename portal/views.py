from django.shortcuts import render_to_response
from django.template import RequestContext
def home(request):
    return render_to_response('home.html', context_instance=RequestContext(request))

'''
import logging
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from forms import RegisterForm, LoginForm, InfoModForm, ForgotPasswordForm
from models import TProfile
from emailtool import EmailTool
from portal.common import getGroupNameByRequest

logger = logging.getLogger(__name__)


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        group = "teachers"
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            invitecode = form.cleaned_data['invitecode']
            if invitecode:
                invitecode.used = True
                invitecode.save()
            user = User.objects.create_user(username, email, password)
            user.groups = (Group.objects.get(name=group),)
            t = TProfile(user=user)
            t.save()
            return redirect('index')
    return render_to_response('register.html', {'form': form},
                              context_instance=RequestContext(request))


@login_required
def index(request):
    group = getGroupNameByRequest(request)
    logger.debug("user group:%s" % group)
    if group == 'teachers':
        return redirect('teacher_index')
    if group == 'students':
        return redirect('student_index')
    messages.add_message(request, messages.INFO, 'User has no permission for broswering, please contact admin')
    return redirect('login')


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        form = LoginForm(request.POST)
        if form.is_valid():
            if __login(request, username, password):
                nextpage = request.GET.get('next')
                if nextpage:
                    return redirect(nextpage)
                else:
                    return redirect('index')
    return render_to_response('login.html', {'form': form},
                              context_instance=RequestContext(request))


def logout(request):
    auth_logout(request)
    return redirect('login')


def __login(request, username, password):
    ret = False
    user = authenticate(username=username, password=password)
    if user:
        if user.is_active:
            auth_login(request, user)
            ret = True
        else:
            messages.add_message(request, messages.INFO, 'User is not active!')
    else:
        messages.add_message(request, messages.INFO, 'User is not existed!')
    return ret


def __mod_user(username, newpassword, newemail):
    u = User.objects.get(username=username)
    u.set_password(newpassword)
    u.email = newemail
    u.save()
    return True


@login_required
def info_modify(request):
    form = InfoModForm(initial={'username': request.user.username})
    if request.method == 'POST':
        form = InfoModForm(request.POST)
        if form.is_valid() and request.user:
            newpassword = form.cleaned_data['newpassword']
            email = form.cleaned_data['email']
            __mod_user(request.user.username, newpassword, email)
            return redirect('index')
    return render_to_response('info_modify.html', {'form': form},
                              context_instance=RequestContext(request))


def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            et = EmailTool()
            et.send([email], "your new password is:sss")
            messages.add_message(request, messages.SUCCESS,
                                 '%s:Your password has been emailed to you!' % username)
            return redirect('login')
    return render_to_response('forgot_password.html', {'form': form},
                              context_instance=RequestContext(request))
'''
