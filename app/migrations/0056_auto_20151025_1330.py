# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0055_auto_20151023_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personcompanyhraplan',
            name='company_hra_plan',
            field=models.ForeignKey(related_name='person_company_hra_plan', blank=True, to='app.CompanyHraPlan', null=True),
            preserve_default=True,
        ),
    ]
