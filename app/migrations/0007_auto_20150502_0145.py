# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20150501_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='company',
            field=models.ForeignKey(related_name='employee_profile_company', default=0, to='app.Company'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='job_title',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='person',
            field=models.ForeignKey(related_name='employee_profile_person', default=0, to='app.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='employeeprofile',
            unique_together=set([('person', 'company')]),
        ),
    ]
