# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_companyintegrationprovider_employee_external_id_seed'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='photo_url',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='pin',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
