# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_employee1095c'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='benefit_start_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
