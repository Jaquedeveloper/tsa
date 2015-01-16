from datetime import datetime

from django.db import models
from queries.models import Query


# Create your models here.

class Tweet(models.Model):
    query = models.OneToOneField(Query)
    text = models.CharField(max_length=140, null=False)
    date = models.CharField(max_length=50, null=False)
    twitter_user = models.CharField(max_length=100, null=False)