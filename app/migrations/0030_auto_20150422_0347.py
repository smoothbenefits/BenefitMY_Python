# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20150418_0439'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companyltdinsuranceplan',
            old_name='elimination_period',
            new_name='elimination_period_in_days',
        ),
        migrations.RenameField(
            model_name='companyltdinsuranceplan',
            old_name='max_benefit',
            new_name='max_benefit_monthly',
        ),
        migrations.RenameField(
            model_name='companystdinsuranceplan',
            old_name='max_benefit',
            new_name='max_benefit_monthly',
        ),
    ]
