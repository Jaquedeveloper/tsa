# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '0002_auto_20150121_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 21, 21, 31, 22, 638439)),
            preserve_default=True,
        ),
    ]
