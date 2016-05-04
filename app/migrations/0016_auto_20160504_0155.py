# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_companyserviceprovider'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyPhraseology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='company_company_phraseology', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmployeePhraseology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('employee_person', models.ForeignKey(related_name='employee_employee_phraseology', to='app.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Phraseology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phraseology', models.CharField(max_length=2048)),
                ('ma_code', models.CharField(max_length=4, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='employeephraseology',
            name='phraseology',
            field=models.ForeignKey(related_name='phraseology_employee_phraseology', to='app.Phraseology'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyphraseology',
            name='phraseology',
            field=models.ForeignKey(related_name='phraseology_company_phraseology', to='app.Phraseology'),
            preserve_default=True,
        ),
    ]
