# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_directdeposit_reminder_of_all'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyFeatureList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyFeatures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_status', models.BooleanField(default=True)),
                ('company', models.ForeignKey(to='app.Company')),
                ('feature', models.ForeignKey(to='app.CompanyFeatureList')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
