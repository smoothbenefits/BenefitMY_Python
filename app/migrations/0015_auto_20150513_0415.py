# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_remove_supplementallifeinsuranceplanrate_condition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplementallifeinsuranceplanrate',
            old_name='condition_key',
            new_name='condition',
        ),
        migrations.AddField(
            model_name='supplementallifeinsuranceplan',
            name='use_employee_age_for_spouse',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
