__author__ = 'joker'
from django.contrib import admin
from queries.models import Query
from tsa.models import Tweet


# Register your models here.

admin.site.register(Query)
admin.site.register(Tweet)