import datetime as dt
from django.db.models import Q
from ..models import Catagory, Staff, Course, Instructor, Module, Participant
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
    participant = Participant.objects.get(pk=request.user.id)
    title += participant.name + "!"
    content = "Daily Notices:"
    return render_to_response('participant/index.html', locals())

@login_required
def course(request):
    counts = dict()
    for c in Catagory.objects.all():
        counts[c] = Course.objects.filter(catagory=c, is_open=True).count()
    return render_to_response('participant/course.html', locals())

@login_required
def catagory_info(request, catagory_id):
    parent_participant = Participant.objects.get(pk=request.user.id)
    parent_catagory = Catagory.objects.get(pk=catagory_id)
    courses = Course.objects.filter(catagory = parent_catagory, is_open = True)
    return render_to_response('participant/catagory_info.html', locals())

@login_required
def course_info(request, course_id):
    participant = Participant.objects.get(pk=request.user.id)
    menu = participant.viewCourse(course_id)
    course_id = course_id
    is_enrolled = menu['is_enrolled']
    title = menu['name']
    catagory = menu['catagory']
    instructor = menu['instructor']
    description = menu['description']
    if is_enrolled:
        modules = menu['module']
    return render_to_response('participant/course_info.html', locals())

@login_required
def enroll(request, course_id):
    participant = Participant.objects.get(pk=request.user.id)
    if participant.enroll(course_id):
        return course_info(request, course_id)
    else:
        return HttpResponse("You cannot enroll in two courses at the same time.")
