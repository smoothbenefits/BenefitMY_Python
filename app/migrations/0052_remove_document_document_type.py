# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0051_remove_template_document_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='document_type',
        ),
    ]
