# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_remove_upload_upload_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companybenefitplanoption',
            name='benefit_option_type',
            field=models.TextField(choices=[(b'individual', b'individual'), (b'individual_plus_spouse', b'individual_plus_spouse'), (b'individual_plus_family', b'individual_plus_family'), (b'individual_plus_children', b'individual_plus_children'), (b'individual_plus_one', b'individual_plus_one')]),
            preserve_default=True,
        ),
    ]
