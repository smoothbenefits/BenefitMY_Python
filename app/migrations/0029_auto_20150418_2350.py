# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_merge'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CompanyFeatureList',
            new_name='SysApplicationFeature',
        ),
        migrations.AlterField(
            model_name='upload',
            name='upload_type',
            field=models.TextField(choices=[(b'I9', b'I9'), (b'Deposit', b'Deposit'), (b'Manager', b'Manager')]),
            preserve_default=True,
        ),
    ]
