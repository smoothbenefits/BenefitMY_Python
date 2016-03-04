# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_emailblocklist'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyServiceProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider_type', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=1024)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=32, null=True, blank=True)),
                ('link', models.CharField(max_length=1024, null=True, blank=True)),
                ('show_to_employee', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='service_provider', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
