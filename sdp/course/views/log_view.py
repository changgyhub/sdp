from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from ..models import Staff, Course, Instructor, Participant, Administrator, HR
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from . import instructor_view as iv, participant_view as pv, administrator_view as av, hr_view as hv
import re
#from django.views.decorators.csrf import csrf_protect, csrf_exempt
#from django.template.context_processors import csrf

# detect the latest group type the current user choose to login


def typeSelect(id):
    if Participant.objects.filter(user__pk=id).exists():
        return Participant.objects.get(user__pk=id).last_login_type
    elif Instructor.objects.filter(user__pk=id).exists():
        return Instructor.objects.get(user__pk=id).last_login_type
    elif HR.objects.filter(user__pk=id).exists():
        return HR.objects.get(user__pk=id).last_login_type
    elif Administrator.objects.filter(user__pk=id).exists():
        return Administrator.objects.get(user__pk=id).last_login_type
    else:
        return "Staff"


def assignType(id, login_type):
    if Participant.objects.filter(user__pk=id).exists():
        role = Participant.objects.get(user__pk=id)
        role.last_login_type = login_type
        role.save()
    if Instructor.objects.filter(user__pk=id).exists():
        role = Instructor.objects.get(user__pk=id)
        role.last_login_type = login_type
        role.save()
    if HR.objects.filter(user__pk=id).exists():
        role = HR.objects.get(user__pk=id)
        role.last_login_type = login_type
        role.save()
    if Administrator.objects.filter(user__pk=id).exists():
        role = Administrator.objects.get(user__pk=id)
        role.last_login_type = login_type
        role.save()


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            last_login_type = typeSelect(request.user.id)
            if last_login_type == "Participant":
                return pv.index(request)
            elif last_login_type == "Instructor":
                return iv.index(request)
            elif last_login_type == "HR":
                return hv.index(request)
            elif last_login_type == "Administrator":
                return av.index(request)
            else:
                return logout(request)
        else:
            return render_to_response('login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        staff_type = request.POST['staff_type']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            if staff_type == "1":
                auth.login(request, user)
                if user.groups.filter(name='Participant').exists():
                    return pv.index(request)
                else:
                    # TODO: wrong access
                    return logout(request)
            elif staff_type == '2':
                auth.login(request, user)
                if user.groups.filter(name='Instructor').exists():
                    return iv.index(request)
                else:
                    # TODO: wrong access
                    return logout(request)
            elif staff_type == '3':
                auth.login(request, user)
                if user.groups.filter(name='HR').exists():
                    return hv.index(request)
                else:
                    # TODO: wrong access
                    return logout(request)
            elif staff_type == '4':
                auth.login(request, user)
                if user.groups.filter(name='Administrator').exists():
                    return av.index(request)
                else:
                    # TODO: wrong access
                    return logout(request)
        else:
            # TODO: password wrong
            return render_to_response('login.html')


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def participant_registration(request):
    username = request.POST['username']
    password = request.POST['password']
    first_name = request.POST['firstname']
    last_name = request.POST['lastname']
    if Participant.objects.filter(user__username=username).exists():
        return render_to_response('login.html', RequestContext(request, {'duplicate_username': True, 'register_again': True}))
    if len(username) != 8 or re.match("^[a-zA-Z0-9_\-]+$", username) is None:
        return render_to_response('login.html', RequestContext(request, {'invalid_username': True, 'register_again': True}))
    user = User.objects.create_user(
        username=username, password=password, first_name=first_name, last_name=last_name)
    g = Group.objects.get(name='Participant')
    g.user_set.add(user)
    Participant.objects.create(user=user, last_login_type='participants')
    return HttpResponse("0")
