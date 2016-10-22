from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.all_courses, name='all_courses'),
    url(r'^course/(?P<course_id>\d+)$', views.course_info, name='course_info'),
]
