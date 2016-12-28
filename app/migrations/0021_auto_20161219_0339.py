# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20161125_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='employee_number',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='employeeprofile',
            unique_together=set([('person', 'company'), ('employee_number', 'company')]),
        ),
    ]
