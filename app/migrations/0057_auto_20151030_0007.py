# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0056_auto_20151025_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company1094cmonthlymemberinfo',
            name='section_4980h_transition_relief',
            field=models.CharField(default=b'', max_length=2),
            preserve_default=True,
        ),
    ]
