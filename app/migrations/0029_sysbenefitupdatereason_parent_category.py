# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_benefitpolicykey_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysbenefitupdatereason',
            name='parent_category',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
