# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20170412_2156'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='employeeprofile',
            unique_together=set([('person', 'company'), ('pin', 'company'), ('employee_number', 'company')]),
        ),
    ]
