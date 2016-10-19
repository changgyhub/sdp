from django.contrib import admin
from .models import Catagory
from .models import Course
from .models import Module
from .models import Component
from .models import Participant
from .models import Instructor
from .models import HistoryEnrollment
from .models import CurrentEnrollment

admin.site.register(Catagory)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Component)
admin.site.register(Participant)
admin.site.register(Instructor)
admin.site.register(HistoryEnrollment)
admin.site.register(CurrentEnrollment)
