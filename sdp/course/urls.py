from django.conf.urls import include, url
from .views import log_view as lv, instructor_view as iv, participant_view as pv
urlpatterns = [
    url(r'^$', lv.login, name='login'),
    url(r'^logout/', lv.logout, name='logout'),
    url(r'^instructor/',include([
        url(r'^catagory/',include([
            url(r'^info/',iv.catagory_info, name='instructor_catagory_info'),
        ])),
        url(r'^course/',include([
            url(r'^create/',include([
                url(r'^finish/', iv.finish_create_course, name='instructor_finish_create_course'),
                url(r'^start/', iv.create_course, name='instructor_create_course'),
            ])),
            url(r'^info/',iv.course_info, name='instructor_course_info'),
            url(r'^open/', iv.open_course, name= 'instructor_open_course'),
            # url(r'^close/', iv.close_course, name= 'instructor_close_course'),
            url(r'^$', iv.course, name='instructor_course'),
        ])),
        url(r'^module/',include([
            url(r'^create/',include([
                url(r'^finish/', iv.finish_create_module, name='instructor_finish_create_module'),
                url(r'^start/', iv.create_module, name='instructor_create_module'),
            ])),
        ])),
        url(r'^component/',include([
            url(r'^create/',include([
                url(r'^finish/', iv.finish_create_component, name='instructor_finish_create_component'),
                url(r'^start/', iv.create_component, name='instructor_create_component'),
            ])),
        ])),
    ])),

    url(r'^participant/',include([
        url(r'^catagory/',include([
            url(r'^info/',pv.catagory_info, name='participant_catagory_info'),
        ])),
        url(r'^course/',include([
            url(r'^enroll/',pv.enroll, name='participant_enroll'),
            url(r'^info/',pv.course_info, name='participant_course_info'),
            url(r'^$', pv.course, name='participant_course'),
        ])),
    ])),
]
