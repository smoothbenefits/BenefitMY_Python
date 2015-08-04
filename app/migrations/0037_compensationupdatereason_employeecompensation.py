# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20150802_0522'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompensationUpdateReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
                ('created_at', models.DateField(default=datetime.datetime.now, auto_now_add=True)),
                ('updated_at', models.DateField(default=datetime.datetime.now, auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmployeeCompensation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('annual_base_salary', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('increase_percentage', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('effective_date', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, auto_now=True)),
                ('person', models.ForeignKey(related_name='employee_compensation_person', blank=True, to='app.Person', null=True)),
                ('reason', models.ForeignKey(related_name='employee_compensation', blank=True, to='app.CompensationUpdateReason', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
