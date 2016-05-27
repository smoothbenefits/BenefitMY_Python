# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20160505_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeephraseology',
            name='end_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeephraseology',
            name='start_date',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
