# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20161229_0248'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDepartment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='company_company_department', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='companydepartment',
            unique_together=set([('company', 'department')]),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='department',
            field=models.ForeignKey(related_name='employee_profile_company_department', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='app.CompanyDepartment', null=True),
            preserve_default=True,
        ),
    ]
