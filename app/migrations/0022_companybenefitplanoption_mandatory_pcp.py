# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20150603_0125'),
    ]

    operations = [
        migrations.AddField(
            model_name='companybenefitplanoption',
            name='mandatory_pcp',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
