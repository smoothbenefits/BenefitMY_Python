# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0052_remove_document_document_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company1094CMemberInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_of_1095c', models.PositiveIntegerField(default=0)),
                ('authoritative_transmittal', models.BooleanField(default=False)),
                ('member_of_aggregated_group', models.BooleanField(default=False)),
                ('certifications_of_eligibility', models.CharField(default=b'Qualifying Offer Method', max_length=50, choices=[(b'Qualifying Offer Method', b'Qualifying Offer Method'), (b'Qualifying Offer Method Transition Relief', b'Qualifying Offer Method Transition Relief'), (b'Section 4980H Transition Relief', b'Section 4980H Transition Relief'), (b'98 Percent Offer Method', b'98 Percent Offer Method')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='company_1094C', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company1094CMonthlyMemberInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minimum_essential_coverage', models.BooleanField(default=False)),
                ('fulltime_employee_count', models.PositiveIntegerField(default=0)),
                ('total_employee_count', models.PositiveIntegerField(default=0)),
                ('aggregated_group', models.BooleanField(default=False)),
                ('section_4980h_transition_relief', models.BooleanField(default=False)),
                ('period', models.CharField(default=b'All 12 Months', max_length=14, choices=[(b'All 12 Months', b'All 12 Months'), (b'Jan', b'Jan'), (b'Feb', b'Feb'), (b'Mar', b'Mar'), (b'Apr', b'Apr'), (b'May', b'May'), (b'June', b'June'), (b'July', b'July'), (b'Aug', b'Aug'), (b'Sept', b'Sept'), (b'Oct', b'Oct'), (b'Nov', b'Nov'), (b'Dec', b'Dec')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='company_1094C_monthly', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
