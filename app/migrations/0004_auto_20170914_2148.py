# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170901_0335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useronboardingstepstate',
            name='step',
            field=models.CharField(max_length=255, choices=[(b'basic_info', b'basic_info'), (b'employment_authorization', b'employment_authorization'), (b'W4_info', b'W4_info'), (b'state_tax_info', b'state_tax_info'), (b'direct_deposit', b'direct_deposit'), (b'documents', b'documents')]),
            preserve_default=True,
        ),
    ]
