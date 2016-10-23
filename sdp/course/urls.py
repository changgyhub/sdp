from django.conf.urls import include, url
from . import views
urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^course/',include([
        url(r'^(?P<course_id>\d+)$',views.course_info, name='course_info'),
    ])),
    url(r'^catagory/',include([
        url(r'^(?P<catagory_id>\d+)$',views.catagory_info, name='catagory_info'),
    ])),
]
