from __future__ import absolute_import

from TwitterAPI import TwitterAPI
from django.conf import settings

from tsa.celery import app


api = TwitterAPI(
    settings.CONSUMER_KEY,
    settings.CONSUMER_SECRET,
    settings.ACCESS_TOKEN,
    settings.ACCESS_TOKEN_SECRET
)


@app.task
def run_query(query_string):
    response = api.request('search/tweets', {'q': query_string})
