# coding=utf-8
"""
    queries.views
"""
import os

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.conf import settings
from textblob import TextBlob

from tsa.celery_app import app
from tsa.utils import json_response
from tsa import tasks
from queries.forms import QueryForm
from queries.models import Query, RunningQuery
from tsa.models import Tweet


@login_required
def create_query(request):
    """

    :param request:
    :return:
    """
    if request.method != 'POST':
        return json_response({
            'status': 'error',
            'message': 'Invalid request type'
        })

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

    return json_response({
        'status': 'error',
        'message': 'Fill all required fields'
    })


@login_required
def edit_query(request):
    """

    :param request:
    :return:
    """
    if request.method != 'POST':
        return json_response({
            'status': 'error',
            'message': 'Invalid request type'
        })

    try:
        query_id = int(request.POST.get('id', ''))
    except ValueError:
        return json_response({
            'status': 'error',
            'message': 'Invalid query id format'
        })

    if request.user.account.is_group_admin:
        query = Query.objects.filter(
            pk=query_id,
            user__account__group=request.user.account.group,
            is_public=True
        )
    else:
        query = Query.objects.filter(pk=query_id, user=request.user)

    if not query.exists():
        return json_response({
            'status': 'error',
            'message': 'You have no permissions to edit this query'
        })

    rq = RunningQuery.objects.filter(query=query)
    if rq.exists():
        return json_response({
            'status': 'error',
            'message': "You can't edit running query"
        })

    query = query.first()

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

    return json_response({
        'status': 'success',
        'query': query.to_dict(),
        'edited': True,
        'message': 'Query successfully edited!'
    })


@login_required
def get_query(request):
    """

    :param request:
    :return:
    """
    try:
        query_id = int(request.POST.get('query_id', ''))
    except ValueError:
        return json_response({
            'status': 'error',
            'message': 'Invalid query id format'
        })

    query = Query.objects.filter(pk=query_id, user=request.user)
    if not query.exists():
        query = Query.objects.filter(
            pk=query_id,
            user__account__group=request.user.account.group
        ).filter(is_public=True)

    if not query.exists():
        return json_response({
            'status': 'error',
            'message': 'Query not found'
        })

    query = query.first()

    return json_response({
        'status': 'success',
        'message': 'Query was found',
        'query': query.to_dict()
    })


@login_required
def delete_query(request):
    """

    :param request:
    :return:
    """
    try:
        query_id = int(request.POST.get('query_id', ''))
    except ValueError:
        return json_response({
            'status': 'error',
            'message': 'Invalid query id format'
        })

    if request.user.account.is_group_admin:
        query = Query.objects.filter(
            pk=query_id,
            user__account__group=request.user.account.group,
            is_public=True
        )
    else:
        query = Query.objects.filter(user=request.user, pk=query_id)

    if not query.exists():
        return json_response({
            'status': 'error',
            'message': 'You have no permissions to delete this query'
        })

    query = query.first()

    rq = RunningQuery.objects.filter(query=query)
    if rq.exists():
        return json_response({
            'status': 'error',
            'message': "You can't delete running query"
        })

    query.delete()
    rq.filter(user=request.user).delete()

    return json_response({
        'status': 'success',
        'message': 'Query was deleted!'
    })


@login_required
def run_query(request):
    """

    :param request:
    :return:
    """
    rq = RunningQuery.objects.filter(user=request.user)
    if rq.exists() > 0:
        return json_response({
            'status': 'error',
            'message': "You can't run more than one query right now"
        })

    try:
        query_id = int(request.POST.get('query_id', ''))
    except ValueError:
        return json_response({
            'status': 'error',
            'message': 'Invalid query id format'
        })

    query = Query.objects.filter(user=request.user, pk=query_id)
    if not query.exists():
        query = Query.objects.filter(
            pk=query_id,
            user__account__group=request.user.account.group,
            is_public=True
        )

    if not query.exists():
        return json_response({
            'status': 'error',
            'message': 'Query not found'
        })

    query = query.first()

    task_id = tasks.get_tweets.delay(query_id, query.to_search_query_string()).id

    rq = RunningQuery()
    rq.user = request.user
    rq.query = query
    rq.task_id = task_id
    rq.save()

    return json_response({
        'status': 'success',
        'message': 'Query was run. Wait for results!'
    })


@login_required
def stop_query(request):
    """

    :param request:
    :return:
    """
    rq = RunningQuery.objects.filter(user=request.user)
    if not rq.exists():
        return json_response({
            'status': 'error',
            'message': 'You have no running queries'
        })

    try:
        query_id = int(request.POST.get('query_id', ''))
    except ValueError:
        return json_response({
            'status': 'error',
            'message': 'Invalid query id format'
        })

    query = Query.objects.filter(user=request.user, pk=query_id)
    if not query.exists():
        query = Query.objects.filter(
            pk=query_id,
            user__account__group=request.user.account.group,
            is_public=True
        )

    if not query.exists():
        return json_response({
            'status': 'error',
            'message': 'Query not found'
        })

    query = query.first()

    rq = rq.filter(query=query)

    if not rq.exists():
        return json_response({
            'status': 'error',
            'message': 'This query was run not by you'
        })

    rq = rq.first()
    app.control.revoke(rq.task_id, terminate=True)
    rq.delete()
    return json_response({
        'status': 'success',
        'message': 'Query was stopped'
    })


@login_required
def get_my_queries(request):
    """

    :param request:
    :return:
    """
    my_queries = Query.objects.filter(user=request.user).order_by('-date')
    queries = [q.to_dict() for q in my_queries]

    rq = RunningQuery.objects.filter(user=request.user)
    running_query_id = None

    if rq.exists():
        rq = rq.first()
        running_query_id = rq.query.id

    return json_response({
        'queries': queries,
        'running_query_id': running_query_id
    })


@login_required
def get_group_queries(request):
    """

    :param request:
    :return:
    """
    if request.user.account.group:
        group_queries = Query.objects.filter(
            user__account__group=request.user.account.group, is_public=True
        ).exclude(
            user=request.user
        ).order_by(
            '-date'
        )
        queries = [q.to_dict() for q in group_queries]

        rq = RunningQuery.objects.filter(user=request.user)
        running_query_id = None

        if rq.exists():
            rq = rq.first()
            running_query_id = rq.query.id

        return json_response({
            'queries': queries,
            'running_query_id': running_query_id
        })
    return json_response({'queries': None})


@login_required
def get_query_results(request):
    """

    :param request:
    :return:
    """
    rq = RunningQuery.objects.filter(user=request.user)
    if not rq.exists():
        try:
            query_id = int(request.POST.get('query_id', ''))
        except ValueError:
            return json_response({
                'status': 'error',
                'message': 'Invalid query id format'
            })
    else:
        rq = rq.first()
        query_id = rq.query.id

    query = Query.objects.filter(user=request.user, pk=query_id)
    if not query.exists():
        query = Query.objects.filter(
            pk=query_id,
            user__account__group=request.user.account.group,
            is_public=True
        )

    if not query.exists():
        return json_response({
            'status': 'error',
            'message': 'Query not found'
        })

    query = query.first()

    tweets = Tweet.objects.filter(query=query).order_by('-date')

    if not tweets.exists():
        return json_response({
            'status': 'error',
            'message': 'No tweets to analyse'
        })

    tweets = [tweet.to_dict() for tweet in tweets]

    full_text = ''
    hashtags = dict()
    users = set()

    for tweet in tweets:
        full_text += tweet['text'] + ' '
        for ht in tweet['hashtags'].split():
            if ht not in hashtags:
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

    return json_response({
        'status': 'success',
        'tweets': tweets,
        'analysis': analysis
    })


@login_required
def filter_tweets(request, query_id, filter_str):
    """

    :param request:
    :param query_id:
    :param filter_str:
    :return:
    """
    try:
        query_id = int(query_id)
    except ValueError:
        raise Http404("Query not found")

    query = Query.objects.filter(user=request.user, pk=query_id)
    if not query.exists():
        query = Query.objects.filter(
            pk=query_id,
            user__account__group=request.user.account.group,
            is_public=True
        )

    if not query.exists():
        raise Http404("Query not found")

    query = query.first()

    tweets = Tweet.objects.filter(query=query, text__icontains=filter_str).order_by('-date')

    if not tweets.exists():
        # TODO no tweets message to template
        pass

    tweets_as_csv = [tweet.as_csv() for tweet in tweets]
    tweets = [tweet.to_dict() for tweet in tweets]

    full_text = ''
    hashtags = dict()
    users = set()

    for tweet in tweets:
        full_text += tweet['text'] + ' '
        for ht in tweet['hashtags'].split():
            if ht not in hashtags:
                hashtags[ht] = 0
            hashtags[ht] += 1
        users.add(tweet['user'])

    tb = TextBlob(full_text)

    keywords = query.all_words + ' ' + query.any_word + ' ' + query.phrase + ' ' + query.users + ' ' + query.hashtags
    keywords = keywords.strip()

    word_counts = sorted(zip(tb.word_counts.values(), tb.word_counts.keys()), reverse=True)
    word_counts = word_counts[:int(len(word_counts) * 0.3)]

    word_counts = [(c, w) for c, w in word_counts if len(w) >= 3]

    hashtag_counts = sorted(zip(hashtags.values(), hashtags.keys()), reverse=True)

    analysis = {
        'word_counts': word_counts,
        'hashtags': hashtag_counts,
        'users': list(users),
        'keywords': keywords
    }

    context = {
        'analysis': analysis,
        'tweets': tweets,
    }

    path = os.path.join(settings.CSV_FILES_ROOT, (query.title.replace(' ', '_')) + ('__' + filter_str))

    with open(path, 'w') as csv:
        csv.write('\n'.join(tweets_as_csv).encode('utf-8'))

    return render(request, 'queries/filter.html', context)


@login_required
def download_csv(request, query_id, filter_str):
    """

    :param request:
    :param query_id:
    :param filter_str:
    :return:
    """
    try:
        query_id = int(query_id)
    except ValueError:
        raise Http404("Query not found")

    query = Query.objects.filter(user=request.user, pk=query_id)
    if not query.exists():
        query = Query.objects.filter(
            pk=query_id,
            user__account__group=request.user.account.group,
            is_public=True
        )

    if not query.exists():
        raise Http404("Query not found")

    query = query.first()

    path = os.path.join(settings.CSV_FILES_ROOT, (query.title.replace(' ', '_')) + ('__' + filter_str))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        (query.title.replace(' ', '_')) + ('__' + filter_str))

    with open(path) as csv:
        response.write(csv.read())

    return response