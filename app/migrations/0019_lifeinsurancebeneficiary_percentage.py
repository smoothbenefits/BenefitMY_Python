# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_person_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='lifeinsurancebeneficiary',
            name='percentage',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
