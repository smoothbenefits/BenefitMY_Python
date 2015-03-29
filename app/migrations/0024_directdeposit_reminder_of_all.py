# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20150318_0143'),
    ]

    operations = [
        migrations.AddField(
            model_name='directdeposit',
            name='remainder_of_all',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
