# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_auto_20150730_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companybenefitplanoption',
            name='employee_cost_per_period',
            field=models.DecimalField(max_digits=20, decimal_places=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companylifeinsuranceplan',
            name='employee_cost_per_period',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personcompsuppllifeinsuranceplan',
            name='child_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated premium for child', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personcompsuppllifeinsuranceplan',
            name='self_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated premium for self', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personcompsuppllifeinsuranceplan',
            name='spouse_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated premium for spouse', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercompanyltdinsuranceplan',
            name='total_premium_per_period',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercompanystdinsuranceplan',
            name='total_premium_per_period',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
    ]
