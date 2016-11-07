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
