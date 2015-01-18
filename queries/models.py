from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

class Query(models.Model):
    title = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.now(), null=False)
    is_public = models.BooleanField(default=False, null=False)
    all_words = models.CharField(max_length=50, null=True, default=None)
    phrase = models.CharField(max_length=50, null=True, default=None)
    any_word = models.CharField(max_length=50, null=True, default=None)
    none_of = models.CharField(max_length=50, null=True, default=None)
    hashtags = models.CharField(max_length=100, null=True, default=None)
    users = models.CharField(max_length=100, null=True, default=None)
    date_from = models.DateField(null=True, default=None)
    date_to = models.DateField(null=True, default=None)

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
            date_from=str(self.date_from) if self.date_from else '',
            date_to=str(self.date_to) if self.date_to else '',
            search_query=self.to_search_query_string()
        )

    def to_search_query_string(self):

        query = ''

        if self.all_words:
            query = self.all_words

        if self.phrase:
            if query:
                query += ' '
            query += '"' + self.phrase + '"'

        if self.any_word:
            if query:
                query += ' '
            query += " OR ".join(self.any_word.split())

        if self.none_of:
            if query:
                query += ' '
            query += " ".join(('-' + word for word in self.none_of.split()))

        if self.hashtags:
            if query:
                query += ' '
            query += " ".join(('#' + word for word in self.hashtags.split()))

        if self.users:
            if query:
                query += ' '
            query += " OR ".join(('from:' + user for user in self.users.split()))

        if self.date_from:
            if query:
                query += ' '
            query += 'since:' + str(self.date_from)

        if self.date_to:
            if query:
                query += ' '
            query += 'until:' + str(self.date_to)

        return query