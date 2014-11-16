# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20141115_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='content',
        ),
        migrations.AlterField(
            model_name='employmentauthorization',
            name='worker_type',
            field=models.CharField(max_length=30, choices=[(b'Citizen', b'Citizen'), (b'Noncitizen', b'Noncitizen'), (b'PResident', b'PResident'), (b'Aaw', b'Aaw')]),
        ),
    ]
