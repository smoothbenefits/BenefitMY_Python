# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20170119_0225'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyUserIntegrationProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_user_external_id', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_user', models.ForeignKey(related_name='integration_provider', to='app.CompanyUser')),
                ('integration_provider', models.ForeignKey(related_name='company_user_list', to='app.IntegrationProvider')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='companyuserintegrationprovider',
            unique_together=set([('company_user', 'integration_provider'), ('company_user_external_id', 'integration_provider')]),
        ),
    ]
