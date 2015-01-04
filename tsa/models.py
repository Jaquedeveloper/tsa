from django.db import models
from datetime import datetime

# Create your models here.

class Query(models.Model):
    title = models.CharField(max_length=100, null=False)
    body = models.CharField(max_length=255, null=False)
    date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.title