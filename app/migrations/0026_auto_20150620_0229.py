# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20150612_0143'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysBenefitUpdateReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fsa',
            name='record_reason',
            field=models.ForeignKey(related_name='fsa_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fsa',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompanyhraplan',
            name='record_reason',
            field=models.ForeignKey(related_name='hra_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompanyhraplan',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='record_reason',
            field=models.ForeignKey(related_name='suppl_life_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanybenefitplanoption',
            name='record_reason',
            field=models.ForeignKey(related_name='health_benefit_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanybenefitplanoption',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanylifeinsuranceplan',
            name='record_reason',
            field=models.ForeignKey(related_name='basic_life_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanylifeinsuranceplan',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanyltdinsuranceplan',
            name='record_reason',
            field=models.ForeignKey(related_name='ltd_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanyltdinsuranceplan',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanystdinsuranceplan',
            name='record_reason',
            field=models.ForeignKey(related_name='std_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanystdinsuranceplan',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanywaivedbenefit',
            name='record_reason',
            field=models.ForeignKey(related_name='health_benefit_waive_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanywaivedbenefit',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
    ]
