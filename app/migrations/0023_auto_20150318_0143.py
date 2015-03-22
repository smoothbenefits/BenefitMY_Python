# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20150317_0012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='w4',
            old_name='total_points',
            new_name='calculated_points',
        ),
        migrations.RenameField(
            model_name='w4',
            old_name='final_points',
            new_name='user_defined_points',
        ),
    ]
