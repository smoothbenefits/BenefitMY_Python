# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20141230_0231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercompanybenefitplanoption',
            name='waived_benefit',
        ),
    ]
