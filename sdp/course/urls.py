from django.conf.urls import include, url
from .views import log_view as lv, instructor_view as iv, participant_view as pv
urlpatterns = [
    url(r'^$', lv.login, name='login'),
    url(r'^logout/', lv.logout, name='logout'),
    url(r'^instructor/',include([
        url(r'^catagory/',include([
            url(r'^(?P<catagory_id>\d+)$',iv.catagory_info, name='instructor_catagory_info'),
        ])),
        url(r'^course/',include([
            url(r'^create/',include([
                url(r'^(?P<catagory_id>\d+)/(?P<course_name>[\w|\W|\d]+)/(?P<course_description>[\w|\W|\d]+)$', iv.finish_create_course, name='instructor_finish_create_course'),
                url(r'^(?P<catagory_id>\d+)$', iv.create_course, name='instructor_create_course'),
            ])),
            url(r'^(?P<course_id>\d+)$',iv.course_info, name='instructor_course_info'),
            url(r'^$', iv.course, name='instructor_course'),
        ])),
        url(r'^module/',include([
            url(r'^create/',include([
                url(r'^(?P<course_id>\d+)/(?P<module_name>[\w|\W|\d]+)$', iv.finish_create_module, name='instructor_finish_create_module'),
                url(r'^(?P<course_id>\d+)$', iv.create_module, name='instructor_create_module'),
            ])),
        ])),
        url(r'^component/',include([
            url(r'^create/',include([
                url(r'^(?P<module_id>\d+)/(?P<component_name>[\w|\W|\d]+)/(?P<component_type>[\w|\W|\d]+)/(?P<component_content>[\w|\W|\d]+)$', iv.finish_create_component, name='instructor_finish_create_component'),
                url(r'^(?P<module_id>\d+)$', iv.create_component, name='instructor_create_component'),
            ])),
        ])),
    ])),

    url(r'^participant/',include([
        url(r'^catagory/',include([
            url(r'^(?P<catagory_id>\d+)$',pv.catagory_info, name='participant_catagory_info'),
        ])),
        url(r'^course/',include([
            url(r'^(?P<course_id>\d+)/enroll$',pv.enroll, name='participant_enroll'),
            url(r'^(?P<course_id>\d+)$',pv.course_info, name='participant_course_info'),
            url(r'^$', pv.course, name='participant_course'),
        ])),
    ])),
]
