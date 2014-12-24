from django.conf.urls import patterns, url
from views import new_user, process_login, show_profile, process_logout

urlpatterns = patterns('',
    url(r'^new/$', new_user, name='new_user'),
    url(r'^login/$', process_login, name='login'),
    url(r'^profile/$', show_profile, name='profile'),
    url(r'^logout/$', process_logout, name='logout')
)