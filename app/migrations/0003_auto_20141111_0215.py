# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20141106_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employmentauthorization',
            name='expiration_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='employmentauthorization',
            name='uscis_number',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
