from datetime import datetime

from django.db import models
from queries.models import Query


# Create your models here.

class Tweet(models.Model):
    query = models.OneToOneField(Query)
    text = models.CharField(max_length=140, null=False, db_index=True)
    date = models.CharField(max_length=50, null=False)
    hashtags = models.CharField(max_length=100, null=True, default=None)
    twitter_user = models.CharField(max_length=100, null=False)