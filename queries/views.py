from django.contrib.auth.decorators import login_required
from textblob import TextBlob

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
    return json_response({'queries': queries, 'running_query_id': request.session.get('running_query_id')})


@login_required
def get_group_queries(request):
    if request.user.account.group:
        group_queries = Query.objects.filter(
            user__account__group=request.user.account.group, is_public=True
        ).exclude(
            user=request.user
        ).order_by(
            '-date'
        )
        queries = [q.to_dict() for q in group_queries]
        return json_response({'queries': queries, 'running_query_id': request.session.get('running_query_id')})
    return json_response({'queries': None})


@login_required
def delete_query(request):
    try:
        query_id = int(request.POST.get('id', ''))
    except ValueError:
        return json_response({'status': 'error'})

    if request.user.account.is_group_admin:
        query = Query.objects.filter(
            pk=query_id, user__account__group=request.user.account.group
        )
    else:
        query = Query.objects.filter(user=request.user, pk=query_id)

    if query:
        query.delete()
        return json_response({'status': 'success'})

    return json_response({'status': 'error'})


@login_required
def run_query(request):
    if request.session.get('running_task_id'):
        return json_response({'status': 'already-running-task'})

    try:
        query_id = int(request.POST.get('query_id', ''))
    except ValueError:
        return json_response({'status': 'error'})

    try:
        query = Query.objects.get(pk=query_id)
    except Query.DoesNotExist:
        return json_response({'status': 'error'})

    task_id = tasks.get_tweets.delay(query_id, query.to_search_query_string()).id

    request.session['running_task_id'] = task_id
    request.session['running_query_id'] = query_id
    return json_response({'status': 'success'})


@login_required
def stop_query(request):
    if not request.session.get('running_task_id'):
        return json_response({'status': 'no-running-query'})

    try:
        query_id = int(request.POST.get('query_id', ''))
    except ValueError:
        return json_response({'status': 'error'})

    try:
        running_query_id = int(request.session.get('running_query_id', ''))
    except ValueError:
        return json_response({'status': 'error'})

    if running_query_id != query_id:
        json_response({'status': 'error'})

    task_id = request.session.get('running_task_id')
    if task_id:
        app.control.revoke(task_id, terminate=True)
        del request.session['running_task_id']
        del request.session['running_query_id']
        return json_response({'status': 'stopped'})

    return json_response({'status': 'no-running-task'})


@login_required
def get_query(request):
    try:
        query_id = int(request.POST.get('query_id', ''))
    except ValueError:
        return json_response({'status': 'error'})

    try:
        query = Query.objects.get(pk=query_id)
    except Query.DoesNotExist:
        return json_response({'status': 'error'})

    return json_response({'status': 'success', 'query': query.to_dict()})


@login_required
def edit_query(request):
    try:
        query_id = int(request.POST.get('id', ''))
    except ValueError:
        return json_response({'status': 'error'})

    try:
        query = Query.objects.get(pk=query_id)
    except Query.DoesNotExist:
        return json_response({'status': 'error'})

    query.title = request.POST.get('title')
    query.all_words = request.POST.get('all_words')
    query.phrase = request.POST.get('phrase')
    query.any_word = request.POST.get('any_word')
    query.none_of = request.POST.get('none_of')
    query.hashtags = request.POST.get('hashtags')
    query.users = request.POST.get('users')
    query.date_from = request.POST.get('date_from') or None
    query.date_to = request.POST.get('date_to') or None
    query.is_public = request.POST.get('is_public') or False


    query.save()

    return json_response({'status': 'success', 'query': query.to_dict(), 'edited': True, 'message': 'Success!'})


@login_required
def get_query_results(request):
    query_id = request.session.get('running_query_id')
    if not query_id:
        try:
            query_id = int(request.POST.get('query_id', ''))
        except ValueError:
            return json_response({'status': 'error'})

    try:
        query = Query.objects.get(pk=query_id)
    except Query.DoesNotExist:
        return json_response({'status': 'error'})

    tweets = Tweet.objects.filter(query=query).order_by('-date')
    tweets = [tweet.to_dict() for tweet in tweets]

    full_text = ''
    hashtags = dict()
    users = set()

    for tweet in tweets:
        full_text += tweet['text'] + ' '
        for ht in tweet['hashtags'].split():
            if not ht in hashtags:
                hashtags[ht] = 0
            hashtags[ht] += 1
        users.add(tweet['user'])

    tb = TextBlob(full_text)

    keywords = query.all_words + ' ' + query.any_word + ' ' + query.phrase + ' ' + query.users + ' ' + query.hashtags
    keywords = keywords.strip()

    word_counts = sorted(zip(tb.word_counts.values(), tb.word_counts.keys()), reverse=True)
    word_counts = word_counts[:int(len(word_counts) * 0.05)]

    word_counts = [(c, w) for c, w in word_counts if len(w) >= 3]

    hashtag_counts = sorted(zip(hashtags.values(), hashtags.keys()), reverse=True)

    analysis = {
        'word_counts': word_counts,
        'hashtags': hashtag_counts,
        'users': list(users),
        'keywords': keywords
    }

    return json_response(
        {
            'status': 'success',
            'tweets': tweets,
            'analysis': analysis
        }
    )