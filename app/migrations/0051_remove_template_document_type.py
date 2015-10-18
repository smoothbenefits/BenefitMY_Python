# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_companyextrabenefitplan_extrabenefititem_personcompanyextrabenefitplan_personcompanyextrabenefitplan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='document_type',
        ),
    ]
