# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_auto_20150919_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyCommuterPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan_name', models.CharField(max_length=255, null=True, blank=True)),
                ('enable_transit_benefit', models.BooleanField(default=False)),
                ('enable_parking_benefit', models.BooleanField(default=False)),
                ('employer_transit_contribution', models.DecimalField(max_digits=20, decimal_places=10)),
                ('employer_parking_contribution', models.DecimalField(max_digits=20, decimal_places=10)),
                ('deduction_period', models.CharField(max_length=30, choices=[(b'Monthly', b'Monthly'), (b'PerPayPeriod', b'PerPayPeriod')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='company_commuter_plan', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonCompanyCommuterPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monthly_amount_transit_pre_tax', models.DecimalField(max_digits=20, decimal_places=10)),
                ('monthly_amount_transit_post_tax', models.DecimalField(max_digits=20, decimal_places=10)),
                ('monthly_amount_parking', models.DecimalField(max_digits=20, decimal_places=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_commuter_plan', models.ForeignKey(related_name='person_company_commuter_plan', to='app.CompanyCommuterPlan')),
                ('person', models.ForeignKey(related_name='person_company_commuter_plan', to='app.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
