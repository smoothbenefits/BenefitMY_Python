# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20150115_0331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefittype',
            name='name',
            field=models.CharField(max_length=255, choices=[(b'Medical', b'Medical'), (b'Dental', b'Dental'), (b'Vision', b'Vision'), (b'Life', b'Life')]),
        ),
    ]
