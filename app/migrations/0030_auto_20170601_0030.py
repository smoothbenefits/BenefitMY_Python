# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_companyuserfeatures'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='companyuserintegrationprovider',
            unique_together=set([('company_user', 'integration_provider')]),
        ),
    ]
