# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_employeeprofile_benefit_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyExtraBenefitPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=4000, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='company_extra_benefit_plan', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtraBenefitItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_plan', models.ForeignKey(related_name='benefit_items', blank=True, to='app.CompanyExtraBenefitPlan', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonCompanyExtraBenefitPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('record_reason_note', models.CharField(max_length=512, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_plan', models.ForeignKey(related_name='person_company_extra_benefit_plan', to='app.CompanyExtraBenefitPlan')),
                ('person', models.ForeignKey(related_name='person_company_extra_benefit_plan', to='app.Person')),
                ('record_reason', models.ForeignKey(related_name='extra_benefits_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonCompanyExtraBenefitPlanItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opt_in', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('extra_benefit_item', models.ForeignKey(related_name='person_company_extra_benefit_plans', to='app.ExtraBenefitItem')),
                ('person_company_extra_benefit_plan', models.ForeignKey(related_name='plan_items', blank=True, to='app.PersonCompanyExtraBenefitPlan', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
