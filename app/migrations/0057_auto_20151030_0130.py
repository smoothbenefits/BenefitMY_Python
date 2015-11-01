# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0056_auto_20151025_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='upload',
            field=models.ForeignKey(related_name='document_uploads', blank=True, to='app.Upload', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='template',
            name='upload',
            field=models.ForeignKey(related_name='template_uploads', blank=True, to='app.Upload', null=True),
            preserve_default=True,
        ),
    ]
