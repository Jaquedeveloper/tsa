# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '0003_auto_20150121_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 34, 29, 108327)),
            preserve_default=True,
        ),
    ]
