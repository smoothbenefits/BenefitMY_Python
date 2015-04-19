# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20150304_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='w4',
            name='extra_amount',
            field=models.DecimalField(default=0, null=True, max_digits=20, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='w4',
            name='final_points',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
