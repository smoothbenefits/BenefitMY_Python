# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20150301_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='companylifeinsuranceplan',
            name='insurance_amount',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lifeinsurancebeneficiary',
            name='tier',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'1', b'1'), (b'2', b'2')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lifeinsuranceplan',
            name='insurance_type',
            field=models.CharField(blank=True, max_length=16, null=True, choices=[(b'Basic', b'Basic'), (b'Extended', b'Extended')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercompanylifeinsuranceplan',
            name='insurance_amount',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
