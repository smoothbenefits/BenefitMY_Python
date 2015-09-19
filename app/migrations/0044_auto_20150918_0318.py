# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_auto_20150917_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='child_adad_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated adad premium for child', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='self_adad_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated adad premium for self', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='spouse_adad_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated adad premium for spouse', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
    ]
