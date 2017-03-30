# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_systemsetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyintegrationprovider',
            name='employee_external_id_seed',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
