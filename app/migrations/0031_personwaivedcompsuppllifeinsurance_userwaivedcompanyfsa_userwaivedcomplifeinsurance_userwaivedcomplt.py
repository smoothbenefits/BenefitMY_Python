# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_sysbenefitupdatereasoncategory_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonWaivedCompSupplLifeInsurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=2048, null=True, blank=True)),
                ('record_reason_note', models.CharField(max_length=512, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='person_waived_suppl_life_comp', to='app.Company')),
                ('company_supplemental_life_insurance_plan', models.ForeignKey(related_name='person_waived_suppl_life', to='app.CompSupplLifeInsurancePlan')),
                ('person', models.ForeignKey(related_name='person_waived_suppl_life_person', to='app.Person')),
                ('record_reason', models.ForeignKey(related_name='suppl_life_waive_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserWaivedCompanyFsa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=2048, null=True, blank=True)),
                ('record_reason_note', models.CharField(max_length=512, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='user_waived_fsa_company', to='app.Company')),
                ('company_fsa', models.ForeignKey(related_name='user_waived_fsa', to='app.CompanyFsaPlan')),
                ('record_reason', models.ForeignKey(related_name='fsa_waive_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True)),
                ('user', models.ForeignKey(related_name='user_waived_fsa_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserWaivedCompLifeInsurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=2048, null=True, blank=True)),
                ('record_reason_note', models.CharField(max_length=512, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='user_waived_life_company', to='app.Company')),
                ('company_life_insurance', models.ForeignKey(related_name='user_waived_basic_life', to='app.CompanyLifeInsurancePlan')),
                ('record_reason', models.ForeignKey(related_name='basic_life_waive_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True)),
                ('user', models.ForeignKey(related_name='user_waived_life_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserWaivedCompLtdInsurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=2048, null=True, blank=True)),
                ('record_reason_note', models.CharField(max_length=512, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='user_waived_ltd_company', to='app.Company')),
                ('company_ltd_insurance', models.ForeignKey(related_name='user_waived_ltd', to='app.CompanyLtdInsurancePlan')),
                ('record_reason', models.ForeignKey(related_name='ltd_waive_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True)),
                ('user', models.ForeignKey(related_name='user_waived_ltd_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserWaivedCompStdInsurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=2048, null=True, blank=True)),
                ('record_reason_note', models.CharField(max_length=512, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='user_waived_std_company', to='app.Company')),
                ('company_std_insurance', models.ForeignKey(related_name='user_waived_std', to='app.CompanyStdInsurancePlan')),
                ('record_reason', models.ForeignKey(related_name='std_waive_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True)),
                ('user', models.ForeignKey(related_name='user_waived_std_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
