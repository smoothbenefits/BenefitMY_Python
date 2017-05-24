# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auto_20170415_0125'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyUserFeatures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_status', models.BooleanField(default=True)),
                ('company_user', models.ForeignKey(to='app.CompanyUser')),
                ('feature', models.ForeignKey(to='app.SysApplicationFeature')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
