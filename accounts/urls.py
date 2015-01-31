from django.conf.urls import patterns, url
from views import registration, _login, profile, _logout, remove_from_group

urlpatterns = patterns('',
    url(r'^group/remove/$', remove_from_group, name=""),
    url(r'^new/$', registration, name='registration'),
    url(r'^login/$', _login, name='login'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^logout/$', _logout, name='logout')
)