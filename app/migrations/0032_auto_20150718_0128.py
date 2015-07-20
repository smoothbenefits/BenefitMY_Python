# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20150716_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fsa',
            name='dependent_amount_per_year',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsa',
            name='primary_amount_per_year',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
