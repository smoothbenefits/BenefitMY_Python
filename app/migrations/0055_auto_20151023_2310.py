# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_auto_20151021_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='signature_type',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
    ]
