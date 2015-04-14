# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_directdeposit_reminder_of_all'),
    ]

    operations = [
        migrations.AddField(
            model_name='companylifeinsuranceplan',
            name='salary_multiplier',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
