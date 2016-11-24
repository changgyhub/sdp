import datetime as dt
from django.db.models import Q
from ..models import Category, Staff, Course, Instructor, Module, HR, CurrentEnrollment, HistoryEnrollment
from django.shortcuts import render_to_response,render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from . import log_view as lv
import collections

@login_required
def index(request):
    lv.assignType(request.user.id, "HR")
    hour = dt.datetime.now().hour
    if hour < 6 or hour > 19:
        title = "Good night, "
    elif hour < 12:
        title = "Good morning, "
    elif hour < 17:
        title = "Good afternoon, "
    else:
        title = "Good evening, "
    hr = HR.objects.get(user__pk=request.user.id)
    title += str(hr) + "!"
    content = "Daily Notices:"
    return render_to_response('hr/index.html', locals())

@login_required
def course(request):
    hr = HR.objects.get(user__pk=request.user.id)
    counts = hr.viewCategories()
    return render_to_response('hr/course.html', locals())

@login_required
def category_info(request):
    category_id = request.POST['category_id']
    parent_hr = HR.objects.get(user__pk=request.user.id)
    parent_category = Category.objects.get(pk=category_id)
    courses = Course.objects.filter(category = parent_category)
    return render_to_response('hr/category_info.html', locals())

@login_required
def course_info(request):
    course_id = request.POST['course_id']
    hr = HR.objects.get(user__pk=request.user.id)
    menu = hr.viewCourse(course_id)
    title = menu['name']
    category = menu['category']
    instructor = menu['instructor']
    description = menu['description']
    is_open = menu['is_open']
    history = HistoryEnrollment.objects.filter(course__id = course_id)
    current = CurrentEnrollment.objects.filter(course__id = course_id)
    if history:
        count_history = len(history)
        historyList = []
        for h in history:
            temp = [h.participant.user.first_name + " " + h.participant.user.last_name, h]
            historyList.append(temp)
        historyList.sort(key=getKey)
    if current:
        count_current = len(current)
        currentList = []
        for c in current:
            progress = getProgress(c.participant, c.course)
            temp = [c.participant.user.first_name + " " + c.participant.user.last_name, c, progress]
            currentList.append(temp)
        currentList.sort(key=getKey)
    return render_to_response('hr/course_info.html', locals())

@login_required
def getAllParticipants(request):
    hr = HR.objects.get(user__pk=request.user.id)
    participants = hr.viewAllParticipants()
    keylist = []
    for key, value in participants.items():
        temp = [value.user.first_name + " " +value.user.last_name, value]
        keylist.append(temp)
    keylist.sort(key=getKey)
    length = len(keylist)
    return render_to_response('hr/participant.html', locals())

def getKey(item):
    return item[0]

@login_required
def participant_info(request):
    participant_id = request.POST['participant_id']
    hr_id = request.POST['hr_id']
    course_id = request.POST['course_id']
    if Course.objects.filter(pk=course_id).exists():
        course = Course.objects.get(pk=course_id)
    hr = HR.objects.get(user__pk=hr_id)
    participant = hr.viewParticipant(participant_id)
    history = participant.getHistoryInfo()
    current = participant.getCurrentInfo()
    if current:
        percentage = getProgress(participant, current)
    return render_to_response('hr/participant_info.html', locals())

def getProgress(participant, current):
    currentEnrollment = CurrentEnrollment.objects.get(participant = participant)
    menu = participant.viewCourse(current.pk)
    modules = collections.OrderedDict(sorted(menu['module'].items(), key=lambda x: x[0].localPosition))
    modules_total_cnt = len(modules)
    component_total_cnt = len(list(modules.items())[currentEnrollment.current_module_num-1][1])
    percentage = 100 * (currentEnrollment.current_module_num - 1 + \
        (currentEnrollment.current_component_num-1)/component_total_cnt) *(1/modules_total_cnt)
    return percentage
