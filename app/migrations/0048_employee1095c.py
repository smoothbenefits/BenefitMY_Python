# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_auto_20150929_0219'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee1095C',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('safe_harbor', models.CharField(max_length=10, null=True, blank=True)),
                ('period', models.CharField(default=b'All 12 Months', max_length=14, choices=[(b'All 12 Months', b'All 12 Months'), (b'Jan', b'Jan'), (b'Feb', b'Feb'), (b'Mar', b'Mar'), (b'Apr', b'Apr'), (b'May', b'May'), (b'June', b'June'), (b'July', b'July'), (b'Aug', b'Aug'), (b'Sept', b'Sept'), (b'Oct', b'Oct'), (b'Nov', b'Nov'), (b'Dec', b'Dec')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='employee_aca_profile_company', to='app.Company')),
                ('person', models.ForeignKey(related_name='employee_aca_profile_person', to='app.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
