from django.db import models

from queries.models import Query


class Tweet(models.Model):
    query = models.ForeignKey(Query, unique=False)
    text = models.CharField(max_length=140, null=False, db_index=True)
    date = models.DateTimeField(null=False)
    hashtags = models.CharField(max_length=100, null=True, default=None)
    twitter_user = models.CharField(max_length=100, null=False)
    tweet_id = models.BigIntegerField(null=False, db_index=True)
    polarity = models.FloatField(null=False)

    def __unicode__(self):
        return u'Tweet #' + unicode(self.tweet_id)

    def to_dict(self):
        return {
            'query': self.pk,
            'text': self.text,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
            'hashtags': self.hashtags,
            'user': self.twitter_user,
            'id': self.tweet_id,
            'polarity': (self.polarity * 5.0)
        }