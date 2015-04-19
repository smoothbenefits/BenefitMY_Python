# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='companybenefitplanoption',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2014, 12, 9), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companybenefitplanoption',
            name='updated_at',
            field=models.DateTimeField(default=datetime.date(2014, 12, 9), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companyuser',
            name='new_employee',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
