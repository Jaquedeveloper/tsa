# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='group',
            field=models.ForeignKey(default=None, to='accounts.Group', null=True),
            preserve_default=True,
        ),
    ]
