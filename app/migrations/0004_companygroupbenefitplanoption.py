# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_companygroupsuppllifeinsuranceplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyGroupBenefitPlanOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_benefit_plan_option', models.ForeignKey(related_name='company_group_benefit_plan_option', to='app.CompanyBenefitPlanOption')),
                ('company_group', models.ForeignKey(related_name='health_benefit_plan_option', to='app.CompanyGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
