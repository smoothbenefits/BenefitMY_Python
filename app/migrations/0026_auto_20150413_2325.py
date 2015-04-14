# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_companyfeaturelist_companyfeatures'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companyfeatures',
            old_name='feature',
            new_name='company_feature',
        ),
    ]
