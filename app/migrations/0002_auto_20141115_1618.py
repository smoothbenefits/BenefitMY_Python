# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyuser',
            name='company_user_type',
            field=models.TextField(choices=[(b'employee', b'employee'), (b'admin', b'admin'), (b'broker', b'broker'), (b'super', b'super')]),
        ),
    ]
