# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0026_auto_20150404_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload_type', models.TextField(choices=[(b'I9', b'I9'), (b'Deposit', b'Deposit')])),
                ('S3', models.CharField(max_length=2048)),
                ('file_name', models.CharField(max_length=2048, null=True, blank=True)),
                ('file_type', models.CharField(max_length=128, null=True, blank=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('company', models.ForeignKey(related_name='company_upload', to='app.Company')),
                ('user', models.ForeignKey(related_name='user_upload', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
