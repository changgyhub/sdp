import datetime as dt
from django.db.models import Q
from ..models import Catagory, Staff, Course, Instructor, Module, HR
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
