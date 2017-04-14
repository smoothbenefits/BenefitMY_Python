# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20160517_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyuser',
            name='company_user_type',
            field=models.TextField(db_index=True, choices=[(b'employee', b'employee'), (b'admin', b'admin'), (b'broker', b'broker'), (b'super', b'super')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='person_type',
            field=models.CharField(max_length=30, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='relationship',
            field=models.CharField(default=b'dependent', max_length=30, db_index=True, choices=[(b'self', b'self'), (b'dependent', b'dependent'), (b'spouse', b'spouse'), (b'child', b'child'), (b'life partner', b'life partner'), (b'ex-spouse', b'ex-spouse'), (b'disabled dependent', b'disabled dependent'), (b'stepchild', b'stepchild')]),
            preserve_default=True,
        ),
    ]
