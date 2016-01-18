# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_companygroupcommuterplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='manager',
            field=models.ForeignKey(related_name='direct_reports', blank=True, to='app.EmployeeProfile', null=True),
            preserve_default=True,
        ),
    ]
