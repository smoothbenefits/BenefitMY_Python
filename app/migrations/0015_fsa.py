# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0014_directdeposit'),
    ]

    operations = [
        migrations.CreateModel(
            name='FSA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_per_year', models.DecimalField(max_digits=8, decimal_places=2)),
                ('update_reason', models.CharField(max_length=1024, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('person', models.ForeignKey(related_name=b'fsa', null=True, blank=True, to='app.Person', unique=True)),
                ('user', models.ForeignKey(related_name=b'fsa', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
