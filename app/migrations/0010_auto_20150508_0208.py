# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20150505_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='relationship',
            field=models.CharField(default=b'dependent', max_length=30, choices=[(b'self', b'self'), (b'dependent', b'dependent'), (b'spouse', b'spouse')]),
            preserve_default=True,
        ),
    ]
