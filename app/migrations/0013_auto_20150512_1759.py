# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20150510_0249'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysSupplLifeInsuranceCondition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='personcompsuppllifeinsuranceplan',
            name='condition',
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='self_condition',
            field=models.ForeignKey(related_name='person_comp_suppl_life_insurance_plan_self', blank=True, to='app.SysSupplLifeInsuranceCondition', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='spouse_condition',
            field=models.ForeignKey(related_name='person_comp_suppl_life_insurance_plan_spouse', blank=True, to='app.SysSupplLifeInsuranceCondition', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='supplementallifeinsuranceplanrate',
            name='condition_key',
            field=models.ForeignKey(related_name='supplemental_life_insurance_plan_rate', default=1, to='app.SysSupplLifeInsuranceCondition'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='supplementallifeinsuranceplanrate',
            name='condition',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
    ]
