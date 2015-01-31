# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 21, 21, 31, 15, 639149)),
            preserve_default=True,
        ),
    ]
