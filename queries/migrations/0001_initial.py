# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 1, 21, 21, 29, 44, 435423))),
                ('is_public', models.BooleanField(default=False)),
                ('all_words', models.CharField(default=None, max_length=50, null=True)),
                ('phrase', models.CharField(default=None, max_length=50, null=True)),
                ('any_word', models.CharField(default=None, max_length=50, null=True)),
                ('none_of', models.CharField(default=None, max_length=50, null=True)),
                ('hashtags', models.CharField(default=None, max_length=100, null=True)),
                ('users', models.CharField(default=None, max_length=100, null=True)),
                ('date_from', models.DateField(default=None, null=True)),
                ('date_to', models.DateField(default=None, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
