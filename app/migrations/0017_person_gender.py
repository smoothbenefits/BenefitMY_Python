# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_fsa'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='gender',
            field=models.CharField(blank=True, max_length=2, null=True, choices=[(b'F', b'F'), (b'M', b'M')]),
            preserve_default=True,
        ),
    ]
