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
    return render_to_response('hr/course_info.html', locals())

@login_required
def participant(request):
    hr = HR.objects.get(user__pk=request.user.id)
    participants = hr.viewAllParticipants()
    return render_to_response('hr/participant.html', locals())

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
    if not history:
        history = {'None': ''}
    current = participant.getCurrentInfo()
    return render_to_response('hr/participant_info.html', locals())
