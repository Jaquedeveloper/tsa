# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=140, db_index=True)),
                ('date', models.DateTimeField()),
                ('hashtags', models.CharField(default=None, max_length=100, null=True)),
                ('twitter_user', models.CharField(max_length=100)),
                ('tweet_id', models.BigIntegerField(db_index=True)),
                ('polarity', models.FloatField()),
                ('query', models.ForeignKey(to='queries.Query')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
