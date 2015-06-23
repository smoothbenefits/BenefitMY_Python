# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20150620_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='reason_for_change',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
