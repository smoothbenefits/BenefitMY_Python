# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20150510_0249'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplementalLifeInsuranceBeneficiary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('middle_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('relationship', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=32, null=True, blank=True)),
                ('percentage', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('tier', models.CharField(blank=True, max_length=1, null=True, choices=[(b'1', b'1'), (b'2', b'2')])),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('person_comp_suppl_life_insurance_plan', models.ForeignKey(related_name='suppl_life_insurance_beneficiary', blank=True, to='app.PersonCompSupplLifeInsurancePlan', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
