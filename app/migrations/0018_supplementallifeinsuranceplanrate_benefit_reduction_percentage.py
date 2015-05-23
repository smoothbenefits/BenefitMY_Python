# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20150521_0141'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplementallifeinsuranceplanrate',
            name='benefit_reduction_percentage',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
