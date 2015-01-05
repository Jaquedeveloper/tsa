from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Query(models.Model):
    title = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User)
    body = models.CharField(max_length=255, null=False)
    date = models.DateTimeField(default=datetime.now())
    is_public = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.pk,
            'title': self.title,
            'body': self.body,
            'date': str(self.date)[:-7],
            'is_public': self.is_public
        }