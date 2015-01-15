# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20150115_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencycontact',
            name='person',
            field=models.ForeignKey(related_name=b'emergency_contact', blank=True, to='app.Person', null=True),
        ),
    ]
