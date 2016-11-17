import datetime as dt
from django.db.models import Q
from ..models import Category, Staff, Course, Instructor, Module, Component
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from . import log_view as lv
from django.core.files.storage import FileSystemStorage
import collections
import os

@login_required
def index(request):
    lv.assignType(request.user.id, "Instructor")
    hour = dt.datetime.now().hour
    if hour < 6 or hour > 19:
        title = "Good night, "
    elif hour < 12:
        title = "Good morning, "
    elif hour < 17:
        title = "Good afternoon, "
    else:
        title = "Good evening, "
    instructor = Instructor.objects.get(user__pk=request.user.id)
    title += str(instructor) + "!"
    content = "Daily Notices:"
    return render_to_response('instructor/index.html', locals())


@login_required
def course(request):
    instructor = Instructor.objects.get(user__pk=request.user.id)
    counts = instructor.viewCategories()
    return render_to_response('instructor/course.html', locals())


@login_required
def category_info(request):
    category_id = request.POST['category_id']
    parent_instructor = Instructor.objects.get(user__pk=request.user.id)
    parent_category = Category.objects.get(pk=category_id)
    mycourses = Course.objects.filter(
        instructor=parent_instructor, category=parent_category)
    othercourses = Course.objects.filter(
        Q(category=parent_category, is_open=True) & ~Q(instructor=parent_instructor))
    # courses = Course.objects.filter(Q(category = parent_category, is_open = True) | Q(category = parent_category, is_open = False, instructor = parent_instructor))
    return render_to_response('instructor/category_info.html', locals())


@login_required
def course_info(request, parent_course_id=None):
    if parent_course_id == None:
        course_id = request.POST['course_id']
    else:  # the case of finish creating component
        course_id = parent_course_id
    instructor = Instructor.objects.get(user__pk=request.user.id)
    menu = instructor.viewCourse(course_id)
    is_open = menu['is_open']
    title = menu['name']
    category = menu['category']
    instructor = menu['instructor']
    description = menu['description']
    if 'module' in menu:
        is_mine = True
        modules = collections.OrderedDict(sorted(menu['module'].items(), key=lambda x: x[0].localPosition))
    else:
        is_mine = False
    return render_to_response('instructor/course_info.html', locals())


@login_required
def create_course(request):
    category_id = request.POST['category_id']
    category = Category.objects.get(pk=category_id)
    return render_to_response('instructor/create_course.html', locals())


@login_required
def create_module(request):
    course_id = request.POST['course_id']
    course = Course.objects.get(pk=course_id)
    return render_to_response('instructor/create_module.html', locals())


@login_required
def create_component(request):
    module_id = request.POST['module_id']
    module = Module.objects.get(pk=module_id)
    course = module.course
    return render_to_response('instructor/create_component.html', locals())


@login_required
def finish_create_course(request):
    category_id = request.POST['category_id']
    course_name = request.POST['course_name']
    course_description = request.POST['course_description']

    # create new course
    instructor = Instructor.objects.get(user__pk=request.user.id)
    category = Category.objects.get(pk=category_id)
    instructor.createCourse(course_name, course_description, category)

    # refresh category list
    counts = dict()
    for c in Category.objects.all():
        counts[c] = Course.objects.filter(category=c).count()
    returnHTML = "<h3>Categories</h3><ul class=\"nav navbar-stacked\">"
    for category, num in counts.items():
        returnHTML += "<li><a onclick=\"getCategoryInfo(\'" + str(category.id) + "\', \'" + category.name + \
            "\')\">" + category.name + \
            "<span class=\"pull-right\">(" + str(num) + ")</span></a></li>"
    returnHTML += "</ul>"
    return HttpResponse(returnHTML)


@login_required

def finish_create_module(request):
    course_id = request.POST['course_id']
    module_name = request.POST['module_name']
    instructor = Instructor.objects.get(user__pk=request.user.id)
    numOfModules = Module.objects.filter(course__pk=course_id).count()
    instructor.createModule(course_id, module_name, numOfModules + 1)
    return course_info(request)


@login_required
def finish_create_component(request):
    module_id = request.POST['module_id']
    component_name = request.POST['component_name']
    component_type = request.POST['component_type']
    component_content = request.POST['component_content']
    instructor = Instructor.objects.get(user__pk=request.user.id)
    numOfComponent = Component.objects.filter(module__pk=module_id).count()
    instructor.createComponent(
        module_id, component_name, component_type, component_content, localPosition=numOfComponent + 1)
    course_id = Module.objects.get(pk=module_id).course.id
    return course_info(request, course_id)


@login_required
def delete_component(request):
    course_id = request.POST['course_id']
    component_id = request.POST['component_id']
    instructor = Instructor.objects.get(user__pk=request.user.id)
    instructor.deleteComponent(component_id)
    return course_info(request, course_id)


@login_required
def open_course(request):
    course_id = request.POST['course_id']
    instructor = Instructor.objects.get(user__pk=request.user.id)
    instructor.openCourse(course_id)
    # TODO: need to change if there is any problem opening course
    return course_info(request, course_id)


@login_required
def close_course(request):
    course_id = request.POST['course_id']
    instructor = Instructor.objects.get(user__pk=request.user.id)
    instructor.closeCourse(course_id)
    return course_info(request, course_id)


@login_required
def file_upload(request):
    # if DEBUG:
    # print(request.POST)
    module_id = request.POST['module_id']
    component_name = request.POST['component_create_name']
    component_type = request.POST['component_create_content_type'][0]
    component_content = request.POST['component_create_content']
    content_file = request.FILES
    instructor = Instructor.objects.get(user__pk=request.user.id)
    numOfComponent = Component.objects.filter(module__pk=module_id).count()
    component = instructor.createComponent(
        module_id, component_name, component_type, component_content, request.FILES, localPosition=numOfComponent + 1)
    myfile = request.FILES['file']
    component.content_file.save(myfile.name, myfile)
    course_id = Module.objects.get(pk=module_id).course.id
    return course_info(request, course_id)


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
def moveup_component(request):
    component_id = request.POST['component_id']
    component = Component.objects.get(pk=component_id)
    localPosition = component.localPosition
    previous_component = Component.objects.get(
        module__id=component.module.pk, localPosition=localPosition - 1)
    component.localPosition = localPosition - 1
    previous_component.localPosition = localPosition
    component.save()
    previous_component.save()
    course_id = Module.objects.get(pk=component.module.pk).course.id
    return course_info(request, course_id)


@login_required
def movedown_component(request):
    component_id = request.POST['component_id']
    component = Component.objects.get(pk=component_id)
    localPosition = component.localPosition
    next_component = Component.objects.get(
        module__id=component.module.pk, localPosition=localPosition + 1)
    component.localPosition = localPosition + 1
    next_component.localPosition = localPosition
    component.save()
    next_component.save()
    course_id = Module.objects.get(pk=component.module.pk).course.id
    return course_info(request, course_id)


@login_required
def moveup_module(request):
    module_id = request.POST['module_id']
    module = Module.objects.get(pk=module_id)
    localPosition = module.localPosition
    previous_module = Module.objects.get(
        course__id=module.course.pk, localPosition=localPosition - 1)
    module.localPosition = localPosition - 1
    previous_module.localPosition = localPosition
    module.save()
    previous_module.save()
    return course_info(request, module.course.pk)


@login_required
def movedown_module(request):
    module_id = request.POST['module_id']
    module = Module.objects.get(pk=module_id)
    localPosition = module.localPosition
    next_module = Module.objects.get(
        course__id=module.course.pk, localPosition=localPosition + 1)
    print('b' * 10)
    module.localPosition = localPosition + 1
    next_module.localPosition = localPosition
    module.save()
    next_module.save()
    return course_info(request, module.course.pk)

@login_required
def getImage(request):
    path = request.GET['path']
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..', path))
    image_data = open(path, "rb").read()
    return HttpResponse(image_data, content_type="image/png")
