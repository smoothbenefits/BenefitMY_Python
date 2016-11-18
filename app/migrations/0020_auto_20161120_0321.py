# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20161030_0226'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='open_enrollment_day',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='open_enrollment_length_in_days',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='open_enrollment_month',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='employment_status',
            field=models.CharField(default=b'Active', max_length=20, choices=[(b'Active', b'Active'), (b'Prospective', b'Prospective'), (b'Terminated', b'Terminated'), (b'OnLeave', b'OnLeave')]),
            preserve_default=True,
        ),
    ]
