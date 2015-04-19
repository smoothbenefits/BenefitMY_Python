# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_signature_signature_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='BenefitDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=1024)),
                ('benefit_plan', models.ForeignKey(related_name=b'benefit_details', blank=True, to='app.CompanyBenefitPlanOption', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BenefitPolicyKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BenefitPolicyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='benefitdetails',
            name='benefit_policy_key',
            field=models.ForeignKey(related_name=b'benefit_details', blank=True, to='app.BenefitPolicyKey', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='benefitdetails',
            name='benefit_policy_type',
            field=models.ForeignKey(related_name=b'benefit_details', blank=True, to='app.BenefitPolicyType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documenttype',
            name='default_content',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='signature',
            name='signature_type',
            field=models.CharField(default='doc_sign', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='ssn',
            field=encrypted_fields.fields.EncryptedTextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='template',
            name='content',
            field=models.TextField(null=True, blank=True),
        ),
    ]
