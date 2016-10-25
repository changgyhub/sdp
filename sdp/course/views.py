import datetime as dt
from .models import Catagory, Staff, Course, Instructor
from .forms import LoginForm
from django.shortcuts import render_to_response,render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_exempt
def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return instrcutor_index(request)
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
                if staff_type == '2':
                    auth.login(request, user)
                    return instrcutor_index(request)
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

def course_info(request, course_id):
    if request.user.is_authenticated():
        course = Course.objects.get(pk=course_id)
        title = course.name
        catagory = course.catagory.name
        instructor = course.instructor.name
        description = course.description
        return render_to_response('course_info.html', locals())
    else:
        return HttpResponseRedirect("/")

def catagory_info(request, catagory_id):
    if request.user.is_authenticated():
        parent_catagory = Catagory.objects.get(pk=catagory_id)
        courses = Course.objects.filter(catagory = parent_catagory, is_open = True)
        return render_to_response('catagory_info.html', locals())
    else:
        return HttpResponseRedirect("/")

def instrcutor_index(request):
    catagories = Catagory.objects.all()
    hour = dt.datetime.now().hour
    if hour < 6 or hour > 19:
        title = "Good night, "
    elif hour < 12:
        title = "Good morning, "
    elif hour < 17:
        title = "Good afternoon, "
    else:
        title = "Good evening, "
    instructor = Instructor.objects.get(pk=request.user.id)
    title += instructor.name + "!"
    content = "Daily Notices:"
    return render_to_response('test.html', locals())
