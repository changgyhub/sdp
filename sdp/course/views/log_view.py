from ..forms import LoginForm
from django.shortcuts import render_to_response,render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from ..models import Staff, Course, Instructor, Participant
from . import instructor_view as iv, participant_view as pv
#from django.views.decorators.csrf import csrf_protect, csrf_exempt
#from django.template.context_processors import csrf

# detect the latest group type the current user choose to login
def typeSelect(id):
    if Participant.objects.filter(user__pk=id).exists():
        return Participant.objects.get(user__pk=id).last_login_type
    elif Instructor.objects.filter(user__pk=id).exists():
        return Instructor.objects.get(user__pk=id).last_login_type
    else:
        return "Invalid"

def assignType(id, login_type):
    if Participant.objects.filter(user__pk=id).exists():
        role = Participant.objects.get(user__pk=id)
        role.last_login_type = login_type
        role.save()
    if Instructor.objects.filter(user__pk=id).exists():
        role = Instructor.objects.get(user__pk=id)
        role.last_login_type = login_type
        role.save()
    else:
        return "Invalid"

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            last_login_type = typeSelect(request.user.id)
            if last_login_type == "Participant":
                return pv.index(request)
            elif last_login_type == "Instructor":
                return iv.index(request)
            else:
                return logout(request)
        else:
            form = LoginForm()
            return render_to_response('login.html', RequestContext(request, {'form': form,}))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            staff_type = request.POST.get('staff_type')
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
                else :
                    # TODO: login for other users
                    return render_to_response('login.html', RequestContext(request, {'form': form,}))
            else:
                return render_to_response('login.html', RequestContext(request, {'form': form,'password_is_wrong':True}))
        else:
            return render_to_response('login.html', RequestContext(request, {'form': form,}))

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
