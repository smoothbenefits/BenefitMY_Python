# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20150718_0128'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysPayPeriodDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('month_factor', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='company',
            name='pay_period_definition',
            field=models.ForeignKey(related_name='sys_pay_period_definition', blank=True, to='app.SysPayPeriodDefinition', null=True),
            preserve_default=True,
        ),
    ]
