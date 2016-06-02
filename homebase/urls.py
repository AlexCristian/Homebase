from django.conf.urls import url
from . import views

app_name = 'homebase'
urlpatterns = [
        url(r'^userdata/$', views.userdata, name="userdata"),
        url(r'^dashboard/$', views.dashboard, name="dashboard"),
        url(r'^register/$', views.register, name="register"),
        url(r'^signin/$', views.signin, name="signin"),
        url(r'^assignment/(?P<assignment_id>[0-9]+)/$',
            views.assignment_details,
            name="assignment_details"),
        url(r'^assignment/(?P<assignment_id>[0-9]+)/delete/$',
            views.assignment_delete,
            name="assignment_delete"),
        url(r'^assignment/new/$',
            views.assignment_new,
            name="assignment_new"),
        url(r'^course/(?P<course_id>[0-9]+)/$',
            views.course_details,
            name="course_details"),
        url(r'^course/new/$',
            views.course_new,
            name="course_new"),
        url(r'^meeting/(?P<course_id>[0-9]+)/$',
            views.list_meetings,
            name="list_meetings"),
        url(r'^meeting/new/$',
            views.meeting_new,
            name="meeting_new"),
        url(r'^meeting/delete/(?P<meeting_id>[0-9]+)/$',
            views.meeting_delete,
            name="meeting_delete"),
]
