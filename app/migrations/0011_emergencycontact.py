# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_usercompanybenefitplanoption_waived_benefit'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('middle_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('relationship', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=32, null=True)),
                ('person', models.ForeignKey(related_name=b'ec', blank=True, to='app.Person', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
