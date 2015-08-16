# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_auto_20150807_0216'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeTimeTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actual_hour_month', models.DateField()),
                ('actual_hour_per_month', models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, auto_now=True)),
                ('company', models.ForeignKey(related_name='employee_timetracking_company', to='app.Company')),
                ('person', models.ForeignKey(related_name='employee_timetracking_person', to='app.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='employeetimetracking',
            unique_together=set([('person', 'company')]),
        ),
        migrations.AddField(
            model_name='employeecompensation',
            name='hourly_rate',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeecompensation',
            name='projected_hour_per_month',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='pay_rate',
            field=models.ForeignKey(related_name='employee_profile_pay_rate', blank=True, to='app.SysPeriodDefinition', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sysperioddefinition',
            name='month_factor',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
