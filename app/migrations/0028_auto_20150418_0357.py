# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0027_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyStdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percentage_of_salary', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('max_benefit', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='company_std_insurance', blank=True, to='app.Company', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('attachment', models.CharField(max_length=2048, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(related_name='std_insurance_plan', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCompanyStdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_std_insurance', models.ForeignKey(related_name='std_insurance', to='app.CompanyStdInsurancePlan')),
                ('user', models.ForeignKey(related_name='user_company_std_insurance_plan', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='std_insurance_plan',
            field=models.ForeignKey(related_name='company_std_insurance', blank=True, to='app.StdInsurancePlan', null=True),
            preserve_default=True,
        ),
    ]
