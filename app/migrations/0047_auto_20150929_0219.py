# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_companycommuterplan_personcompanycommuterplan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='employment_type',
            field=models.CharField(blank=True, max_length=30, null=True, choices=[(b'FullTime', b'FullTime'), (b'PartTime', b'PartTime'), (b'Contractor', b'Contractor'), (b'Intern', b'Intern'), (b'PerDiem', b'PerDiem')]),
            preserve_default=True,
        ),
    ]
