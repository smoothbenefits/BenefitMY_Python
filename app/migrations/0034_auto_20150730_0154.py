# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20150721_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='pay_period_definition',
            field=models.ForeignKey(related_name='sys_pay_period_definition', default=2, to='app.SysPeriodDefinition'),
            preserve_default=True,
        ),
    ]
