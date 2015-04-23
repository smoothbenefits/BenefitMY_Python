# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companystdinsuranceplan',
            old_name='max_benefit_monthly',
            new_name='max_benefit_weekly',
        ),
    ]
