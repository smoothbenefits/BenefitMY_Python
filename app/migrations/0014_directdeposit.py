# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0013_auto_20150115_0331'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectDeposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('routing1', models.CharField(max_length=32)),
                ('account1', models.CharField(max_length=32)),
                ('account_type1', models.TextField(choices=[(b'Checking', b'Checking'), (b'Saving', b'Saving')])),
                ('bank_name1', models.CharField(max_length=128, null=True, blank=True)),
                ('attachment1', models.CharField(max_length=2048, null=True, blank=True)),
                ('amount1', models.DecimalField(default=0, null=True, max_digits=20, decimal_places=2, blank=True)),
                ('percentage1', models.DecimalField(default=0, null=True, max_digits=5, decimal_places=2, blank=True)),
                ('routing2', models.CharField(max_length=32, null=True, blank=True)),
                ('account2', models.CharField(max_length=32, null=True, blank=True)),
                ('account_type2', models.TextField(blank=True, null=True, choices=[(b'Checking', b'Checking'), (b'Saving', b'Saving')])),
                ('bank_name2', models.CharField(max_length=128, null=True, blank=True)),
                ('attachment2', models.CharField(max_length=2048, null=True, blank=True)),
                ('amount2', models.DecimalField(default=0, null=True, max_digits=20, decimal_places=2, blank=True)),
                ('percentage2', models.DecimalField(default=0, null=True, max_digits=5, decimal_places=2, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(related_name=b'direct_deposit', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
