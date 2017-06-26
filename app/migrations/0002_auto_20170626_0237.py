# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_squashed_0030_auto_20170601_0030'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDivision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('division', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('code', models.CharField(max_length=32, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='company_company_division', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('code', models.CharField(max_length=32, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='company_company_job', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='companyjob',
            unique_together=set([('company', 'job')]),
        ),
        migrations.AlterUniqueTogether(
            name='companydivision',
            unique_together=set([('company', 'division')]),
        ),
        migrations.AddField(
            model_name='companydepartment',
            name='code',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='division',
            field=models.ForeignKey(related_name='employee_profile_company_division', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='app.CompanyDivision', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='job',
            field=models.ForeignKey(related_name='employee_profile_company_job', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='app.CompanyJob', null=True),
            preserve_default=True,
        ),
    ]
