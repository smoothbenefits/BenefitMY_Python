# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20150501_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyfsaplan',
            name='company',
            field=models.ForeignKey(related_name='company_fsa_plan_company', to='app.Company'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companyfsaplan',
            name='fsa_plan',
            field=models.ForeignKey(related_name='company_fsa_plan_fsa_plan', to='app.FsaPlan'),
            preserve_default=True,
        ),
    ]
