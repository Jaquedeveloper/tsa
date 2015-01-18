from django.conf.urls import patterns, url
from queries.views import create_query, get_my_queries, delete_query, run_query, get_query_results


urlpatterns = patterns(
    '',
    url(r'^results/$', get_query_results, name='query_results'),
    url(r'^run/$', run_query, name="run_query"),
    url(r'^delete/$', delete_query, name="delete_query"),
    url(r'^new/$', create_query, name='create_query'),
    url(r'^my/$', get_my_queries, name="my_queries")
)