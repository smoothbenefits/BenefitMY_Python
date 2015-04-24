# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadApplicationFeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_id', models.IntegerField()),
                ('application_feature', models.ForeignKey(related_name='upload_application_feature_app_feature', to='app.SysApplicationFeature')),
                ('upload', models.ForeignKey(related_name='upload_application_feature_upload', to='app.Upload')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UploadAudience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(related_name='upload_audience_company', to='app.Company')),
                ('upload', models.ForeignKey(related_name='upload_audience_upload', to='app.Upload')),
                ('user_for', models.ForeignKey(related_name='upload_audience_user_for', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
