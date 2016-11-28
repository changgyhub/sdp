
from django.conf.urls import include, url
from .views import log_view as lv, instructor_view as iv, participant_view as pv, hr_view as hv, administrator_view as av
urlpatterns = [
    url(r'^$', lv.login, name='login'),
    url(r'^registration/', lv.participant_registration, name='participant_registration'),
    url(r'^logout/', lv.logout, name='logout'),
    url(r'^instructor/',include([
        url(r'^category/',include([
            url(r'^info/',iv.category_info, name='instructor_category_info'),
        ])),
        url(r'^course/',include([
            url(r'^create/',include([
                url(r'^finish/', iv.finish_create_course, name='instructor_finish_create_course'),
                url(r'^start/', iv.create_course, name='instructor_create_course'),
            ])),
            url(r'^info/',iv.course_info, name='instructor_course_info'),
            url(r'^open/', iv.open_course, name= 'instructor_open_course'),
            url(r'^close/', iv.close_course, name= 'instructor_close_course'),
            url(r'^image/', iv.getImage, name='instructor_get_image'),
            url(r'^$', iv.course, name='instructor_course'),
        ])),
        url(r'^module/',include([
            url(r'^create/',include([
                url(r'^finish/', iv.finish_create_module, name='instructor_finish_create_module'),
                url(r'^start/', iv.create_module, name='instructor_create_module'),
            ])),
            url(r'^moveup/', iv.moveup_module, name='instructor_moveup_module'),
            url(r'^movedown/', iv.movedown_module, name='instructor_movedown_module'),
        ])),
        url(r'^component/',include([
            url(r'^create/',include([
                url(r'^finish/', iv.finish_create_component, name='instructor_finish_create_component'),
                url(r'^start/', iv.create_component, name='instructor_create_component'),
                url(r'^upload/', iv.file_upload, name='instructor_file_upload'),

            ])),
            url(r'^download/', iv.file_download, name='instructor_file_download'),
            url(r'^delete/', iv.delete_component, name='instructor_create_component'),
            url(r'^moveup/', iv.moveup_component, name='instructor_moveup_component'),
            url(r'^movedown/', iv.movedown_component, name='instructor_movedown_component'),
        ])),
    ])),

    url(r'^participant/',include([
        url(r'^category/',include([
            url(r'^info/',pv.category_info, name='participant_category_info'),
        ])),
        url(r'^course/',include([
            url(r'^finish/',include([
                url(r'^component/', pv.finish_component, name='participant_finish_component'),
            ])),
            url(r'^drop/',pv.drop, name='participant_drop'),
            url(r'^enroll/',pv.enroll, name='participant_enroll'),
            url(r'^info/',pv.course_info, name='participant_course_info'),
            url(r'^image/', pv.getImage, name='participant_get_image'),
            url(r'^$', pv.course, name='participant_course'),
        ])),
        url(r'^component/',include([
            url(r'^download/', pv.file_download, name='participant_file_download'),
        ])),
    ])),

    url(r'^hr/',include([
        url(r'^category/',include([
            url(r'^info/',hv.category_info, name='hr_category_info'),
        ])),
        url(r'^course/',include([
            url(r'^info/',hv.course_info, name='hr_course_info'),
            url(r'^$', hv.course, name='hr_course'),
        ])),
        url(r'^participant/',include([
            url(r'^info/',hv.participant_info, name='hr_participant_info'),
            url(r'^$', hv.getAllParticipants, name='hr_allParticipants'),
        ])),
    ])),

    url(r'^administrator/', include([
        url(r'^category/', include([
            url(r'^$', av.category, name='administrator_category'),
            url(r'^info',av.category_info, name='administrator_category_info'),
            url(r'^create/', av.category_create, name='administrator_create_category'),
            url(r'^createFinish/', av.category_create_finish, name='administrator_create_finish'),
            url(r'^delete/',av.category_delete, name='administrator_delete_category'),
        ])),
        url(r'^priority/', include([
            url(r'^$', av.priority, name='administrator_priority'),
            url(r'^generate/', av.generate_user, name='administrator_generate'),
            url(r'^designate/', av.designate, name='administrator_designate'),
            url(r'^generate_by_name/', av.generate_by_name, name='administrator_generate_by_name'),
        ])),
    ])),
]
