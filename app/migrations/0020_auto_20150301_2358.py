# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_lifeinsurancebeneficiary_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercompanywaivedbenefit',
            name='reason',
            field=models.CharField(max_length=2048, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanywaivedbenefit',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
    ]
