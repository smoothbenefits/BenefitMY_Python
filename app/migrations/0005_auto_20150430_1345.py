# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150428_0327'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyFsaPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FsaPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('broker_user', models.ForeignKey(related_name='fsa_plan', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companyfsaplan',
            name='fsa_plan',
            field=models.ForeignKey(to='app.FsaPlan'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fsa',
            name='company_fsa_plan',
            field=models.ForeignKey(related_name='company_fsa_plan', to='app.CompanyFsaPlan', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsa',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 30, 13, 45, 1, 938000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsa',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 30, 13, 45, 1, 938000), auto_now=True),
            preserve_default=True,
        ),
    ]
