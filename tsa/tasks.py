from __future__ import absolute_import

import time

from TwitterAPI import TwitterAPI
from django.conf import settings

from tsa.models import Tweet
from queries.models import Query
from tsa.celery_app import app

from datetime import datetime

api = TwitterAPI(
    settings.TWITTER_CONSUMER_KEY,
    settings.TWITTER_CONSUMER_SECRET,
    settings.TWITTER_ACCESS_TOKEN,
    settings.TWITTER_ACCESS_TOKEN_SECRET
)


@app.task(ignore_result=True)
def get_tweets(query_id, query_string):
    try:
        count = 100

        while True:

            tweets = api.request(
                'search/tweets',
                {
                    'q': query_string,
                    'result_type': 'recent',
                    'language': 'en',
                    'count': count
                }
            )

            for t in tweets:
                if not t['retweeted']:
                    if Tweet.objects.filter(tweet_id=t['id']).exists():
                        continue
                    tweet = Tweet()
                    tweet.query = Query.objects.get(pk=query_id)
                    tweet.text = t['text']
                    print t['created_at']
                    tweet.date = datetime.strptime(t['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    hashtags = ' '.join((hashtag['text'] for hashtag in t['entities']['hashtags']))
                    tweet.hashtags = hashtags
                    tweet.twitter_user = t['user']['screen_name'] + ' (' + t['user']['name'] + ')'
                    tweet.tweet_id = t['id']
                    tweet.save()
            if count == 100:
                count = 5

            time.sleep(5)

    except Exception as e:
        print(e.message)