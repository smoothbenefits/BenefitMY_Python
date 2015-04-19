# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companybenefitplanoption',
            name='benefit_option_type',
            field=models.TextField(choices=[(b'individual', b'individual'), (b'individual_plus_spouse', b'individual_plus_spouse'), (b'individual_plus_family', b'individual_plus_family'), (b'individual_plus_children', b'individual_plus_children')]),
        ),
    ]
