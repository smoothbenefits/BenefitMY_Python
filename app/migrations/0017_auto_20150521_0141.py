# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20150517_0328'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='employer_contribution_percentage',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='employer_contribution_percentage',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanyltdinsuranceplan',
            name='total_premium_per_period',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanystdinsuranceplan',
            name='total_premium_per_period',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
