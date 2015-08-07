# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20150802_0522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercompanyltdinsuranceplan',
            old_name='total_premium_per_period',
            new_name='total_premium_per_month',
        ),
        migrations.RenameField(
            model_name='usercompanystdinsuranceplan',
            old_name='total_premium_per_period',
            new_name='total_premium_per_month',
        ),
    ]
