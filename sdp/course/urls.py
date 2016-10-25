from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^instructor/',include([
        url(r'^course/',include([
            url(r'^$', views.instructor_course, name='instructor_course'),
            url(r'^(?P<course_id>\d+)$',views.instructor_course_info, name='instructor_course_info'),
        ])),
        url(r'^catagory/',include([
            url(r'^(?P<catagory_id>\d+)$',views.instructor_catagory_info, name='instructor_catagory_info'),
        ])),
    ])),
]
