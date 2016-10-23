from django.shortcuts import render
from django.http import HttpResponse
from .models import Catagory
from .models import Course
from django.shortcuts import render_to_response

def index(request):
    catagories = Catagory.objects.all()
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
