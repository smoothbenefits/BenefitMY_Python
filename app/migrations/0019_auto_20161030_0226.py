# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20161013_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadForUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload', models.ForeignKey(related_name='upload_for_user_upload', to='app.Upload')),
                ('user_for', models.ForeignKey(related_name='upload_for_user_user_for', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='uploadaudience',
            name='company',
        ),
        migrations.RemoveField(
            model_name='uploadaudience',
            name='upload',
        ),
        migrations.RemoveField(
            model_name='uploadaudience',
            name='user_for',
        ),
        migrations.DeleteModel(
            name='UploadAudience',
        ),
    ]
