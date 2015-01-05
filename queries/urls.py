from django.conf.urls import patterns, url
from queries.views import create_query, get_my_queries


urlpatterns = patterns('',
    url(r'^new/$', create_query, name='create_query'),
    url(r'^my/$', get_my_queries, name="my_queries")
)