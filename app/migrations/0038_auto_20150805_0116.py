# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_auto_20150805_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='relationship',
            field=models.CharField(default=b'dependent', max_length=30, choices=[(b'self', b'self'), (b'dependent', b'dependent'), (b'spouse', b'spouse'), (b'child', b'child'), (b'life partner', b'life partner'), (b'ex-spouse', b'ex-spouse'), (b'disabled dependent', b'disabled dependent'), (b'stepchild', b'stepchild')]),
            preserve_default=True,
        ),
    ]
