import datetime as dt
from django.db.models import Q
from ..models import Category, Staff, Course, Instructor, Module
from ..forms import DocumentForm
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
    mycourses = Course.objects.filter(instructor = parent_instructor, category = parent_category)
    othercourses = Course.objects.filter(Q(category = parent_category, is_open= True) & ~Q(instructor = parent_instructor))
    # courses = Course.objects.filter(Q(category = parent_category, is_open = True) | Q(category = parent_category, is_open = False, instructor = parent_instructor))
    return render_to_response('instructor/category_info.html', locals())


@login_required
def course_info(request, parent_course_id = None):
    if parent_course_id == None:
        course_id = request.POST['course_id']
    else: # the case of finish creating component
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
        modules = menu['module']
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
        returnHTML += "<li><a onclick=\"getCategoryInfo(\'" + str(category.id) + "\', \'" + category.name + "\')\">" + category.name + "<span class=\"pull-right\">(" + str(num) + ")</span></a></li>"
    returnHTML += "</ul>"
    return HttpResponse(returnHTML)

@login_required
def finish_create_module(request):
    course_id = request.POST['course_id']
    module_name = request.POST['module_name']
    instructor = Instructor.objects.get(user__pk=request.user.id)
    instructor.createModule(course_id, module_name)
    return course_info(request)

@login_required
def finish_create_component(request):
    module_id = request.POST['module_id']
    component_name = request.POST['component_name']
    component_type = request.POST['component_type']
    component_content = request.POST['component_content']
    instructor = Instructor.objects.get(user__pk=request.user.id)
    instructor.createComponent(module_id, component_name, component_type, component_content)
    course_id = Module.objects.get(pk=module_id).course.id
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
    module_id = request.POST['module_id']
    if module_id == '#':
        form = DocumentForm()
        return render_to_response('instructor/file_upload.html', locals())
    else:
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            print('gg')