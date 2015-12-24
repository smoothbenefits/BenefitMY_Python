# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151219_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companygrouphsaplan',
            name='company_group',
            field=models.ForeignKey(related_name='company_hsa_plan', to='app.CompanyGroup'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personcompanygrouphsaplan',
            name='company_hsa_plan',
            field=models.ForeignKey(related_name='person_hsa_selection', blank=True, to='app.CompanyHsaPlan', null=True),
            preserve_default=True,
        ),
    ]
