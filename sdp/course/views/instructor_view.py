import datetime as dt
from django.db.models import Q
from ..models import Catagory, Staff, Course, Instructor, Module
from django.shortcuts import render_to_response,render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
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
    return render_to_response('instructor/index.html', locals())

@login_required
def course(request):
    instructor = Instructor.objects.get(pk=request.user.id)
    counts = dict()
    for c in Catagory.objects.all():
        counts[c] = Course.objects.filter(Q(catagory=c) & (Q(is_open=True) | Q(instructor=instructor))).count()
    return render_to_response('instructor/course.html', locals())


@login_required
def catagory_info(request, catagory_id):
    parent_instructor = Instructor.objects.get(pk=request.user.id)
    parent_catagory = Catagory.objects.get(pk=catagory_id)
    courses = Course.objects.filter(Q(catagory = parent_catagory, is_open = True) | Q(catagory = parent_catagory, is_open = False, instructor = parent_instructor))
    return render_to_response('instructor/catagory_info.html', locals())


@login_required
def course_info(request, course_id):
    instructor = Instructor.objects.get(pk=request.user.id)
    menu = instructor.viewCourse(course_id)
    course_id = course_id
    is_open = menu['is_open']
    title = menu['name']
    catagory = menu['catagory']
    instructor = menu['instructor']
    description = menu['description']
    if 'module' in menu:
        is_mine = True
        modules = menu['module']
    else:
        is_mine = False
    return render_to_response('instructor/course_info.html', locals())

@login_required
def create_course(request, catagory_id):
    catagory = Catagory.objects.get(pk=catagory_id)
    return render_to_response('instructor/create_course.html', locals())

@login_required
def create_module(request, course_id):
    course = Course.objects.get(pk=course_id)
    return render_to_response('instructor/create_module.html', locals())

@login_required
def create_component(request, module_id):
    module = Module.objects.get(pk=module_id)
    return render_to_response('instructor/create_component.html', locals())

@login_required
def finish_create_course(request, catagory_id, course_name, course_description):
    # create new course

    instructor = Instructor.objects.get(pk=request.user.id)
    catagory = Catagory.objects.get(pk=catagory_id)
    instructor.createCourse(course_name, course_description, catagory)

    # refresh catagory list
    counts = dict()
    for c in Catagory.objects.all():
        counts[c] = Course.objects.filter(catagory=c).count()
    returnHTML = "<h3>Categories</h3><ul class=\"nav navbar-stacked\">"
    for catagory, num in counts.items():
        returnHTML += "<li><a onclick=\"getCatagoryInfo(\'" + str(catagory.id) + "\', \'" + catagory.name + "\')\">" + catagory.name + "<span class=\"pull-right\">(" + str(num) + ")</span></a></li>"
    returnHTML += "</ul>"
    return HttpResponse(returnHTML)

@login_required
def finish_create_module(request, course_id, module_name):
    instructor = Instructor.objects.get(pk=request.user.id)
    instructor.createModule(course_id, module_name)
    return course_info(request, course_id)

@login_required
def finish_create_component(request, module_id, component_name, component_type, component_content):
    instructor = Instructor.objects.get(pk=request.user.id)
    instructor.createComponent(module_id, component_name, component_type, component_content)
    course_id = Module.objects.get(pk=module_id).course.id
    return course_info(request, course_id)
