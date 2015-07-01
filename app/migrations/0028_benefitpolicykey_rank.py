# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_person_reason_for_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='benefitpolicykey',
            name='rank',
            field=models.IntegerField(default=9999),
            preserve_default=True,
        ),
    ]
