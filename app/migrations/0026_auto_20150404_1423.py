# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_companylifeinsuranceplan_salary_multiplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercompanylifeinsuranceplan',
            old_name='life_insurance',
            new_name='company_life_insurance',
        ),
    ]
