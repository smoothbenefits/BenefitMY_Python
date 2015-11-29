# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_auto_20151105_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='companylifeinsuranceplan',
            name='employee_contribution_percentage',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companylifeinsuranceplan',
            name='total_cost_rate',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
    ]
