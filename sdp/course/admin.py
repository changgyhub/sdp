from django.contrib import admin
from .models import Category, Course, Module, Component, Participant, Instructor, HistoryEnrollment, CurrentEnrollment, Administrator, HR

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Component)
admin.site.register(Participant)
admin.site.register(Instructor)
admin.site.register(HistoryEnrollment)
admin.site.register(CurrentEnrollment)
admin.site.register(Administrator)
admin.site.register(HR)
