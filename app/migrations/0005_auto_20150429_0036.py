# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150428_0327'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyFsaPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(blank=True, to='app.Company', null=True)),
                ('fsa_plan', models.ForeignKey(blank=True, to='app.FSA', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCompanyFsaPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_fsa_plan', models.ForeignKey(related_name='user_company_fsa_plan', to='app.CompanyFsaPlan')),
                ('user', models.ForeignKey(related_name='user_company_fsa_plan', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='fsa',
            old_name='user',
            new_name='broker_user',
        ),
    ]
