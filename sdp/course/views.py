from django.shortcuts import render
from django.http import HttpResponse
from .models import Catagory
from .models import Course
def index(request):
    output = []
    menu = dict()
    for catagory in Catagory.objects.all():
        menu[catagory.name] = list()
    for course in Course.objects.all():
        if course.is_open == True:
            menu[course.catagory.name].append(course)
    for key, values in menu.items():
        html = '<p>'+ key
        for value in values:
            html += '<br><a href="/course/'+ str(value.id) +'">&nbsp>&nbsp' + value.name + '</a>'
        html += '</p>'
        output.append(html)
    return HttpResponse('<hr>'.join(output))
def view(request, course_id):
    course = Course.objects.get(pk=course_id)
    html = """ <h1> {name} </h1>
            <p><b>{catagory}</b><br>{instructor}</p>
            <p>Info: {description}</p>"""
    output = html.format(name = course.name, catagory = course.catagory.name, \
                        instructor = course.instructor.name, description = course.description)
    return HttpResponse(output)
