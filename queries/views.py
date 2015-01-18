from django.contrib.auth.decorators import login_required

from celery_app import app
from tsa.utils import json_response
from tsa import tasks
from queries.forms import QueryForm
from queries.models import Query
from tsa.models import Tweet


@login_required
def create_query(request):
    if request.method != 'POST':
        return json_response({'status': 'error', 'message': 'Invalid request type'})

    form = QueryForm(request.POST)
    if form.is_valid():
        query = Query(**form.cleaned_data)
        query.user = request.user
        query.is_public = form.cleaned_data['is_public'] == u'True'
        query.save()
        return json_response({
            'status': 'success',
            'message': 'Query successfully created',
            'query': query.to_dict()
        })

    return json_response({'status': 'error', 'message': 'Fill required fields'})


@login_required
def get_my_queries(request):
    my_queries = Query.objects.filter(user=request.user).order_by('-date')
    queries = [q.to_dict() for q in my_queries]
    return json_response({'queries': queries})


@login_required
def delete_query(request):
    try:
        id = int(request.POST.get('id'))
    except:
        return json_response({'status': 'error'})

    query = Query.objects.filter(user=request.user, pk=id)
    if query:
        query.delete()
        return json_response({'status': 'success'})

    return json_response({'status': 'error'})


@login_required
def run_query(request):
    try:
        query_id = int(request.POST.get('query_id', ''))
    except ValueError:
        return json_response({'status': 'error'})

    try:
        query = Query.objects.get(pk=query_id)
    except Query.DoesNotExist:
        return json_response({'status': 'error'})

    task_id = request.session.get('running_task_id')
    if task_id:
        app.control.revoke(task_id, terminate=True)
        del request.session['running_task_id']
        del request.session['running_query_id']
        return json_response({'status': 'stopped'})

    task_id = tasks.get_tweets.delay(query_id, query.to_search_query_string()).id

    request.session['running_task_id'] = task_id
    request.session['running_query_id'] = query_id

    return json_response({'status': 'running'})


@login_required
def get_query_results(request):
    query_id = request.session.get('running_query_id')
    if not query_id:
        return json_response({'status': 'error'})

    tweets = Tweet.objects.filter(query_id=query_id)
    tweets = [tweet.to_dict() for tweet in tweets]

    return json_response(tweets)