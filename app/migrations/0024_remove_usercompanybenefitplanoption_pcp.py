# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_benefitplan_pcp_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercompanybenefitplanoption',
            name='pcp',
        ),
    ]
