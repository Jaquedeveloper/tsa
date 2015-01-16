from __future__ import absolute_import

from TwitterAPI import TwitterAPI
from django.conf import settings

from tsa.models import Tweet
from tsa.celery import app


api = TwitterAPI(
    settings.CONSUMER_KEY,
    settings.CONSUMER_SECRET,
    settings.ACCESS_TOKEN,
    settings.ACCESS_TOKEN_SECRET
)


@app.task
def run_query(query):
    tweets = api.request(
        'search/tweets',
        {
            'q': query.to_search_query_string(),
            'result_type': 'recent'
        }
    )

    for t in tweets:
        if not t['retweeted']:
            tweet = Tweet()
            tweet.query = query
            tweet.text = t['text']
            tweet.date = t['created_at']
            hashtags = ' '.join((hashtag['text'] for hashtag in t['entities']['hashtags']))
            tweet.hashtags = hashtags
            tweet.twitter_user = t['user']['screen_name'] + '(' + t['user']['name'] + ')'