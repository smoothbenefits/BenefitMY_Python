# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0052_remove_document_document_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='signature_type',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
    ]
