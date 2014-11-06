# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20141105_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='signature',
            field=models.ForeignKey(blank=True, to='app.Signature', null=True),
            preserve_default=True,
        ),
    ]
