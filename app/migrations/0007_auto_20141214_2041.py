# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20141210_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefitdetails',
            name='benefit_plan',
            field=models.ForeignKey(related_name=b'benefit_details', blank=True, to='app.BenefitPlan', null=True),
        ),
    ]
