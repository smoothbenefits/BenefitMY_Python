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
                ('amount', models.DecimalField(default=0, null=True, max_digits=20, decimal_places=2, blank=True)),
                ('percentage', models.DecimalField(default=0, null=True, max_digits=5, decimal_places=2, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserBankAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('routing', models.CharField(max_length=32)),
                ('account', models.CharField(max_length=32)),
                ('account_type', models.TextField(choices=[(b'Checking', b'Checking'), (b'Saving', b'Saving')])),
                ('bank_name', models.CharField(max_length=128, null=True, blank=True)),
                ('attachment', models.CharField(max_length=2048, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(related_name=b'user_bank_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='directdeposit',
            name='bank_account',
            field=models.ForeignKey(related_name=b'direct_deposit', to='app.UserBankAccount'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='directdeposit',
            name='user',
            field=models.ForeignKey(related_name=b'direct_deposit', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
