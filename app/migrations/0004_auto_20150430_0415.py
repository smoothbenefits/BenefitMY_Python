# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_uploadapplicationfeature_uploadaudience'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_title', models.CharField(max_length=50, null=True, blank=True)),
                ('annual_base_salary', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('employment_type', models.CharField(blank=True, max_length=30, null=True, choices=[(b'FullTime', b'FullTime'), (b'PartTime', b'PartTime'), (b'Contractor', b'Contractor'), (b'Intern', b'Intern')])),
                ('employment_status', models.CharField(blank=True, max_length=20, null=True, choices=[(b'Active', b'Active'), (b'Prospective', b'Prospective'), (b'Terminated', b'Terminated'), (b'OnLeave', b'OnLeave')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='employee_profile_company', to='app.Company')),
                ('person', models.ForeignKey(related_name='employee_profile_person', to='app.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='employeeprofile',
            unique_together=set([('person', 'company')]),
        ),
        migrations.AlterField(
            model_name='upload',
            name='upload_type',
            field=models.TextField(choices=[(b'I9', b'I9'), (b'Deposit', b'Deposit'), (b'Manager', b'Manager'), (b'MedicalBenefit', b'MedicalBenefit'), (b'DentalBenefit', b'DentalBenefit'), (b'VisionBenefit', b'VisionBenefit')]),
            preserve_default=True,
        ),
    ]
