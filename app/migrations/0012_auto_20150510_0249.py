# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20150509_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyltdinsuranceplan',
            name='rate',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companystdinsuranceplan',
            name='rate',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True),
            preserve_default=True,
        ),
    ]
