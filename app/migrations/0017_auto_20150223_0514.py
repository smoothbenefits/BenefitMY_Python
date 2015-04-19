# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_fsa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companylifeinsuranceplan',
            name='benefit_option_type',
            field=models.TextField(blank=True, null=True, choices=[(b'individual', b'individual'), (b'individual_plus_spouse', b'individual_plus_spouse'), (b'individual_plus_family', b'individual_plus_family'), (b'individual_plus_children', b'individual_plus_children')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companylifeinsuranceplan',
            name='employee_cost_per_period',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companylifeinsuranceplan',
            name='total_cost_per_period',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
