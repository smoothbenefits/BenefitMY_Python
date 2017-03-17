# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20170313_0100'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=127)),
                ('value', models.CharField(max_length=1023, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
