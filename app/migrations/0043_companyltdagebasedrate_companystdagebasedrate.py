# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_company1095c'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyLtdAgeBasedRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age_min', models.SmallIntegerField(null=True, verbose_name=b'Min value of age.', blank=True)),
                ('age_max', models.SmallIntegerField(null=True, verbose_name=b'Max value of age.', blank=True)),
                ('rate', models.DecimalField(max_digits=20, decimal_places=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_ltd_insurance_plan', models.ForeignKey(related_name='company_ltd_insurance_plan', to='app.CompanyLtdInsurancePlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyStdAgeBasedRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age_min', models.SmallIntegerField(null=True, verbose_name=b'Min value of age.', blank=True)),
                ('age_max', models.SmallIntegerField(null=True, verbose_name=b'Max value of age.', blank=True)),
                ('rate', models.DecimalField(max_digits=20, decimal_places=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_std_insurance_plan', models.ForeignKey(related_name='company_std_insurance_plan', to='app.CompanyStdInsurancePlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
