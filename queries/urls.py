# coding=utf-8
from django.conf.urls import patterns, url

from queries.views import create_query, get_my_queries, delete_query, run_query, get_query_results, stop_query, \
    get_group_queries, get_query, edit_query, filter_tweets, download_csv


urlpatterns = patterns(
    '',
    url(r'^filter/(?P<query_id>\d+)/(?P<filter_str>[a-zA-Z\d]+)/$', filter_tweets, name="tweets_filter"),
    url(r'^filter/(?P<query_id>\d+)/(?P<filter_str>[a-zA-Z\d]+)/csv/$', download_csv, name="tweets_filter"),
    url(r'^get/$', get_query, name="get_query"),
    url(r'^edit/$', edit_query, name="edit_query"),
    url(r'^group/$', get_group_queries, name='group_queries'),
    url(r'^stop/$', stop_query, name='stop_query'),
    url(r'^results/$', get_query_results, name='query_results'),
    url(r'^run/$', run_query, name="run_query"),
    url(r'^delete/$', delete_query, name="delete_query"),
    url(r'^new/$', create_query, name='create_query'),
    url(r'^my/$', get_my_queries, name="my_queries")
)