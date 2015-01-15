from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Query(models.Model):
    title = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.now(), null=False)
    is_public = models.BooleanField(default=False, null=False)
    all_words = models.CharField(max_length=50, null=True)
    phrase = models.CharField(max_length=50, null=True)
    any_word = models.CharField(max_length=50, null=True)
    none_of = models.CharField(max_length=50, null=True)
    hashtags = models.CharField(max_length=100, null=True)
    users = models.CharField(max_length=100, null=True)
    date_from = models.DateField(null=True)
    date_to = models.DateField(null=True)

    def __unicode__(self):
        return self.title

    def to_dict(self):
        return dict(
            id=self.pk,
            title=self.title,
            date=self.date.strftime("%Y-%m-%d %H:%M:%S"),
            is_public=self.is_public,
            all_words=self.all_words,
            phrase=self.phrase,
            any_word=self.any_word,
            none_of=self.none_of,
            hashtags=self.hashtags,
            users=self.users,
            date_from=self.date_from,
            date_to=self.date_to
        )