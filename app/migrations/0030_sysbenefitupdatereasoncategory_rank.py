# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20150703_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysbenefitupdatereasoncategory',
            name='rank',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
