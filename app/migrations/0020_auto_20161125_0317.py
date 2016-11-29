# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20161030_0226'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenEnrollmentDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_month', models.IntegerField()),
                ('start_day', models.IntegerField()),
                ('end_month', models.IntegerField()),
                ('end_day', models.IntegerField()),
                ('company', models.ForeignKey(related_name='employment_authorization', to='app.Company', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='employment_status',
            field=models.CharField(default=b'Active', max_length=20, choices=[(b'Active', b'Active'), (b'Prospective', b'Prospective'), (b'Terminated', b'Terminated'), (b'OnLeave', b'OnLeave')]),
            preserve_default=True,
        ),
    ]
