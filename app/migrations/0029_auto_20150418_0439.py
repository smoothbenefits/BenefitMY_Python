# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0028_auto_20150418_0357'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyLtdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('elimination_period', models.IntegerField(null=True, blank=True)),
                ('duration', models.IntegerField(null=True, blank=True)),
                ('percentage_of_salary', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('max_benefit', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='company_ltd_insurance', blank=True, to='app.Company', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LtdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('attachment', models.CharField(max_length=2048, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(related_name='ltd_insurance_plan', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCompanyLtdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_ltd_insurance', models.ForeignKey(related_name='ltd_insurance', to='app.CompanyLtdInsurancePlan')),
                ('user', models.ForeignKey(related_name='user_company_ltd_insurance_plan', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='ltd_insurance_plan',
            field=models.ForeignKey(related_name='company_ltd_insurance', blank=True, to='app.LtdInsurancePlan', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='duration',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
