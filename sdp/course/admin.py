from django.contrib import admin
from .models import Category, Course, Module, Component, Content, Text, File, Image, YouTube, Participant, Instructor, HistoryEnrollment, CurrentEnrollment, Administrator, HR

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Component)
admin.site.register(Content)
admin.site.register(Text)
admin.site.register(File)
admin.site.register(Image)
admin.site.register(YouTube)
admin.site.register(Participant)
admin.site.register(Instructor)
admin.site.register(HistoryEnrollment)
admin.site.register(CurrentEnrollment)
admin.site.register(Administrator)
admin.site.register(HR)
