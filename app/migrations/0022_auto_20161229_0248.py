# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20161219_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyIntegrationProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_external_id', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='integration_provider', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IntegrationProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('service_type', models.CharField(max_length=30, choices=[(b'Payroll', b'Payroll')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='integrationprovider',
            unique_together=set([('name', 'service_type')]),
        ),
        migrations.AddField(
            model_name='companyintegrationprovider',
            name='integration_provider',
            field=models.ForeignKey(related_name='company_list', to='app.IntegrationProvider'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='companyintegrationprovider',
            unique_together=set([('company', 'integration_provider'), ('company_external_id', 'integration_provider')]),
        ),
    ]
