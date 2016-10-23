from django.shortcuts import render
from django.http import HttpResponse
from .models import Catagory
from .models import Course
from django.shortcuts import render_to_response
import datetime as dt

def index(request):
    title = "Welcome to AB Credit (HK) Staff Development Platform!"
    return render_to_response('index.html', locals())

def course_info(request, course_id):
    course = Course.objects.get(pk=course_id)
    title = course.name
    catagory = course.catagory.name
    instructor = course.instructor.name
    description = course.description
    return render_to_response('course_info.html', locals())

def catagory_info(request, catagory_id):
    parent_catagory = Catagory.objects.get(pk=catagory_id)
    courses = Course.objects.filter(catagory = parent_catagory, is_open = True)
    return render_to_response('catagory_info.html', locals())

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
    title += "instructor!"
    content = "Daily Notices:"
    return render_to_response('instrcutor_index.html', locals())
