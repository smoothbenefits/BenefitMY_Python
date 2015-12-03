# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0062_companygroupmember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companygroupmember',
            name='company_group',
            field=models.ForeignKey(related_name='company_group_member', to='app.CompanyGroup'),
            preserve_default=True,
        ),
    ]
