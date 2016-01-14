# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_companygroupltdinsuranceplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyGroupFsaPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_fsa_plan', models.ForeignKey(related_name='company_group_fsa', to='app.CompanyFsaPlan')),
                ('company_group', models.ForeignKey(related_name='fsa_plan', to='app.CompanyGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
