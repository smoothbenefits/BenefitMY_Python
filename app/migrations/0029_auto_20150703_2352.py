# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_benefitpolicykey_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysBenefitUpdateReasonCategory',
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
            model_name='sysbenefitupdatereason',
            name='category',
            field=models.ForeignKey(related_name='benefit_update_reason_category', blank=True, to='app.SysBenefitUpdateReasonCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sysbenefitupdatereason',
            name='detail_required',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
