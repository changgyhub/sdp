import datetime as dt
from django.db.models import Q
from ..models import Category, Staff, Course, Instructor, Module, Participant, Administrator
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
    lv.assignType(request.user.id, "Administrator")
    hour = dt.datetime.now().hour
    if hour < 6 or hour > 19:
        title = "Good night, "
    elif hour < 12:
        title = "Good morning, "
    elif hour < 17:
        title = "Good afternoon, "
    else:
        title = "Good evening, "
    administrator = Administrator.objects.get(user__pk=request.user.id)
    # no need to check, this method is guaranteed to work
    title += str(administrator) + "!"
    content = "Daily Notices:"
    return render_to_response('administrator/index.html', locals())

@login_required
def category(request):
    admin = Administrator.objects.get(user__pk=request.user.id)
    counts = admin.viewCategories()
    return render_to_response('administrator/category.html',locals())

@login_required
def priority(request):
    admin = Administrator.objects.get(user__pk=request.user.id)
    all = admin.viewAllUsers()

    allUD = dict()
    allUsers = []
    cnt=0
    allUsers.append(allUD)
    for u in all:
        allUsers[cnt][u.pk]=u.username
        if len(allUsers[cnt])==10:
            allUD = dict()
            allUsers.append(allUD)
            cnt+=1
    num = range(len(allUsers))
    return render_to_response('administrator/priority.html',locals())

@login_required
def category_info(request):
    category_id = request.POST['category_id']
    parent_admin = Administrator.objects.get(user__pk=request.user.id)
    parent_category = Category.objects.get(pk=category_id)
    mycourses = Course.objects.filter(instructor = parent_admin, category = parent_category)
    othercourses = Course.objects.filter(Q(category = parent_category, is_open= True) & ~Q(instructor = parent_admin))
    # courses = Course.objects.filter(Q(category = parent_category, is_open = True) | Q(category = parent_category, is_open = False, instructor = parent_instructor))
    return render_to_response('instructor/category_info.html', locals())

@login_required
def category_create(request):
    return render_to_response('administrator/create_category.html', locals())


@login_required
def category_create_finish(request):
    category_name = request.POST['category_name']
    admin = Administrator.objects.get(user__pk=request.user.id)
    admin.createCategory(category_name)
    return

@login_required
def category_delete(request):
    category_name = request.POST['category_name']
    admin = Administrator.objects.get(user__pk=request.user.id)
    if admin.deleteCategory(category_name):
        counts = admin.viewCategories()
        return render_to_response('administrator/delete_category_true.html', locals())
    else:
        counts = admin.viewCategories()
        return render_to_response('administrator/delete_category_false.html', locals())

@login_required
def generate_user(request):
    i = request.POST['i']
    allUsers = request.POST['allUsers']
    return render_to_response('administrator/generateUsersForm.html', locals())