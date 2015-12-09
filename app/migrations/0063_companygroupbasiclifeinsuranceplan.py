# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_companygroupmember'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyGroupBasicLifeInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_basic_life_insurance_plan', models.ForeignKey(related_name='company_group_basic_life_insurance', to='app.CompanyLifeInsurancePlan')),
                ('company_group', models.ForeignKey(related_name='basic_life_insurance_plan', to='app.CompanyGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
