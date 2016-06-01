from django.conf.urls import url
from . import views

app_name = 'homebase'
urlpatterns = [
        url(r'^(?P<user_id>[0-9]+)/$', views.userdata, name="userdata"),
        url(r'^(?P<user_id>[0-9]+)/dashboard/$',
            views.dashboard, name="dashboard")
]
