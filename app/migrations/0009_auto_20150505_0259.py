# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20150503_0058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companyltdinsuranceplan',
            old_name='elimination_period_in_days',
            new_name='elimination_period_in_months',
        ),
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='paid_by',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'Employee', b'Employee'), (b'Employer', b'Employer')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='rate',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='elimination_period_in_days',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='paid_by',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'Employee', b'Employee'), (b'Employer', b'Employer')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='rate',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
