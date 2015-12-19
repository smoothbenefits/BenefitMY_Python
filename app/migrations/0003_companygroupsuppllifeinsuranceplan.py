# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20151211_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyGroupSupplLifeInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_group', models.ForeignKey(related_name='suppl_life_insurance_plan', to='app.CompanyGroup')),
                ('company_suppl_life_insurance_plan', models.ForeignKey(related_name='company_group_suppl_life_insurance', to='app.CompSupplLifeInsurancePlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
