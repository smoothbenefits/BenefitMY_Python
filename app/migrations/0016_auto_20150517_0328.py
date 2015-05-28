# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20150513_0415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplementallifeinsuranceplanrate',
            name='supplemental_life_insurance_plan',
            field=models.ForeignKey(related_name='supplemental_life_insurance_plan_rate', blank=True, to='app.SupplementalLifeInsurancePlan', null=True),
            preserve_default=True,
        ),
    ]
