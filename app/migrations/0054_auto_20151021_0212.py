# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_company1094cmemberinfo_company1094cmonthlymemberinfo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personcompanycommuterplan',
            old_name='monthly_amount_parking',
            new_name='monthly_amount_parking_pre_tax',
        ),
        migrations.AddField(
            model_name='personcompanycommuterplan',
            name='monthly_amount_parking_post_tax',
            field=models.DecimalField(default=0, max_digits=20, decimal_places=10),
            preserve_default=False,
        ),
    ]
