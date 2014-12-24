from django.conf.urls import patterns, include, url
from views import new_user, process_login

urlpatterns = patterns('',
    url(r'^new/$', new_user, name='new_user'),
    url(r'^login/$', process_login, name='login'),
)