# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_company1095c'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='benefit_amount_step',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='require_user_select_amount',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='benefit_amount_step',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='require_user_select_amount',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanyltdinsuranceplan',
            name='user_select_amount',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanystdinsuranceplan',
            name='user_select_amount',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
    ]
