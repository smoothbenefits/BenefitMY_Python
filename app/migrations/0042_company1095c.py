# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0041_auto_20150819_0259'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company1095C',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('offer_of_coverage', models.CharField(max_length=2, null=True, blank=True)),
                ('employee_share', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('safe_harbor', models.CharField(max_length=10, null=True, blank=True)),
                ('period', models.CharField(default=b'All 12 Months', max_length=14, choices=[(b'All 12 Months', b'All 12 Months'), (b'Jan', b'Jan'), (b'Feb', b'Feb'), (b'Mar', b'Mar'), (b'Apr', b'Apr'), (b'May', b'May'), (b'June', b'June'), (b'July', b'July'), (b'Aug', b'Aug'), (b'Sept', b'Sept'), (b'Oct', b'Oct'), (b'Nov', b'Nov'), (b'Dec', b'Dec')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(related_name='company_1095C', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
