# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_companygroupbenefitplanoption'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyGroupStdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_group', models.ForeignKey(related_name='company_std_insurance_plan', to='app.CompanyGroup')),
                ('company_std_insurance_plan', models.ForeignKey(related_name='company_group_std', to='app.CompanyStdInsurancePlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
