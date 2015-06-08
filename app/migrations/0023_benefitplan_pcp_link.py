# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_benefitplan_mandatory_pcp'),
    ]

    operations = [
        migrations.AddField(
            model_name='benefitplan',
            name='pcp_link',
            field=models.CharField(max_length=2048, null=True, blank=True),
            preserve_default=True,
        ),
    ]
