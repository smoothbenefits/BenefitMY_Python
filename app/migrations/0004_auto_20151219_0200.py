# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_companygroupsuppllifeinsuranceplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyGroupHsaPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_group', models.ForeignKey(related_name='company_group_hsa_plan', to='app.CompanyGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyHsaPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='company_hsa_plan', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonCompanyGroupHsaPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_per_year', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('record_reason_note', models.CharField(max_length=512, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_hsa_plan', models.ForeignKey(related_name='company_hsa_plan', blank=True, to='app.CompanyHsaPlan', null=True)),
                ('person', models.ForeignKey(related_name='hsa_plan_person', to='app.Person')),
                ('record_reason', models.ForeignKey(related_name='hsa_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companygrouphsaplan',
            name='company_hsa_plan',
            field=models.ForeignKey(related_name='company_group_hsa_plan', to='app.CompanyHsaPlan'),
            preserve_default=True,
        ),
    ]
