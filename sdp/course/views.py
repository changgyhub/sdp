from django.shortcuts import render
from django.http import HttpResponse
from .models import Catagory
from .models import Course
from django.shortcuts import render_to_response

def course_info(request, course_id):
    course = Course.objects.get(pk=course_id)
    title = course.name
    catagory = course.catagory.name
    instructor = course.instructor.name
    description = course.description
    return render_to_response('course_info.html', locals())

def all_courses(request):
    menu = dict()
    for catagory in Catagory.objects.all():
        menu[catagory.name] = list()
    for course in Course.objects.filter(is_open = True):
        menu[course.catagory.name].append(course)
    return render_to_response('index.html', locals())
