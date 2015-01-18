from __future__ import absolute_import

import time

from TwitterAPI import TwitterAPI
from django.conf import settings

from tsa.models import Tweet
from tsa.celery_app import app


api = TwitterAPI(
    settings.TWITTER_CONSUMER_KEY,
    settings.TWITTER_CONSUMER_SECRET,
    settings.TWITTER_ACCESS_TOKEN,
    settings.TWITTER_ACCESS_TOKEN_SECRET
)


@app.task
def get_tweets(query_id, query_string):
    try:
        count = 100

        while True:

            tweets = api.request(
                'search/tweets',
                {
                    'q': query_string,
                    'result_type': 'recent',
                    'count': count
                }
            )

            for t in tweets:
                if not t['retweeted']:
                    if Tweet.objects.filter(tweet_id=t['id']).exists():
                        continue
                    tweet = Tweet()
                    tweet.query_id = query_id
                    tweet.text = t['text']
                    tweet.date = t['created_at']
                    hashtags = ' '.join((hashtag['text'] for hashtag in t['entities']['hashtags']))
                    tweet.hashtags = hashtags
                    tweet.twitter_user = t['user']['screen_name'] + '(' + t['user']['name'] + ')'
                    tweet.tweet_id = t['id']
                    tweet.save()
            if count == 100:
                count = 5

            time.sleep(5)

    except Exception as e:
        print(e.message)