import datetime as dt
from django.db.models import Q
from ..models import Category, Staff, Course, Instructor, Module, HR, Participant, Facade
from django.shortcuts import render_to_response,render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.template import RequestContext
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

def registration(request):
    user = request.POST['username']
    userpassword = request.POST['userpassword']
    
    