import datetime as dt
from django.db.models import Q
from ..models import Category, Staff, Course, Instructor, Module, Participant, Component, HistoryEnrollment, CurrentEnrollment
from django.shortcuts import render_to_response,render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
import collections, os
from . import log_view as lv

@login_required
def index(request):
    lv.assignType(request.user.id, "Participant")
    hour = dt.datetime.now().hour
    if hour < 6 or hour > 19:
        title = "Good night, "
    elif hour < 12:
        title = "Good morning, "
    elif hour < 17:
        title = "Good afternoon, "
    else:
        title = "Good evening, "
    participant = Participant.objects.get(user__pk=request.user.id)
    title += str(participant) + "!"
    content = "Daily Notices:"
    return render_to_response('participant/index.html', locals())

@login_required
def course(request):
    participant = Participant.objects.get(user__pk=request.user.id)
    counts = participant.viewCategories()
    return render_to_response('participant/course.html', locals())

@login_required
def category_info(request):
    category_id = request.POST['category_id']
    participant_id = Participant.objects.get(user__pk=request.user.id).id
    has_current_course = False
    parent_category = Category.objects.get(pk=category_id)
    if CurrentEnrollment.objects.filter(participant__id = participant_id, course__category = parent_category, course__is_open = True).exists():
        current_course = CurrentEnrollment.objects.get(participant__id = participant_id, course__category = parent_category, course__is_open = True).course
        has_current_course = True
    if HistoryEnrollment.objects.filter(participant__id = participant_id, course__category = parent_category, course__is_open = True).exists():
        history_courses = []
        for he in HistoryEnrollment.objects.filter(participant__id = participant_id, course__category = parent_category, course__is_open = True):
            history_courses.append(he.course)
    all_courses = Course.objects.filter(category = parent_category, is_open = True)
    return render_to_response('participant/category_info.html', locals())

@login_required
def course_info(request):
    course_id = request.POST['course_id']
    participant = Participant.objects.get(user__pk=request.user.id)
    menu = participant.viewCourse(course_id)
    is_enrolled = menu['is_enrolled']
    has_finished = menu['has_finished']
    title = menu['name']
    category = menu['category']
    instructor = menu['instructor']
    description = menu['description']
    if is_enrolled:
        enrollment = CurrentEnrollment.objects.get(participant=participant)
        modules = collections.OrderedDict(sorted(menu['module'].items(), key=lambda x: x[0].localPosition))
        modules_total_cnt = len(modules)
        component_total_cnt = len(list(modules.items())[enrollment.current_module_num-1][1])
        percentage = int(100 * (enrollment.current_module_num - 1 + \
            (enrollment.current_component_num-1)/component_total_cnt) *(1/modules_total_cnt))
    if has_finished:
        modules = collections.OrderedDict(sorted(menu['module'].items(), key=lambda x: x[0].localPosition))
        percentage = 100
    return render_to_response('participant/course_info.html', locals())

@login_required
def enroll(request):
    course_id = request.POST['course_id']
    participant = Participant.objects.get(user__pk=request.user.id)
    if participant.enroll(course_id):
        return course_info(request)
    else:
        # TODO: make it more like a warning
        return HttpResponse("You cannot enroll in two courses at the same time.")

@login_required
def drop(request):
    participant = Participant.objects.get(user__pk=request.user.id)
    participant.drop()
    return course_info(request)

@login_required
def file_download(request):
    component_id = request.GET['component_id']
    component = Component.objects.get(pk=component_id)
    filename = component.content_file.name
    myfile = open(component.content_file.path, "rb")
    response = HttpResponse(myfile, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

@login_required
def getImage(request):
    path = request.GET['path']
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..', path))
    image_data = open(path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")

@login_required
def finish_component(request):
    enrollment = CurrentEnrollment.objects.get(pk=request.POST['enrollment_id'])
    current_module_num = int(request.POST['current_module_num'])
    current_component_num = int(request.POST['current_component_num'])
    total_module_num = int(request.POST['total_module_num'])
    total_component_num = int(request.POST['total_component_num'])

    end_flag = False

    if current_component_num < total_component_num:
        enrollment.current_component_num = enrollment.current_component_num + 1
    elif current_module_num < total_module_num:
        enrollment.current_module_num = enrollment.current_module_num + 1
        enrollment.current_component_num = 1
    else:
        end_flag = True
        enrollment.current_component_num = enrollment.current_component_num + 1
    enrollment.save()

    if end_flag:
        participant = Participant.objects.get(user__pk=request.user.id)
        participant.finishCourse();

    return course_info(request)
