# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20150508_0208'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompSupplLifeInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='comp_suppl_life_insurance_plan', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonCompSupplLifeInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('self_elected_amount', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('spouse_elected_amount', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('child_elected_amount', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
                ('self_premium_per_month', models.DecimalField(null=True, verbose_name=b'calculated premium for self', max_digits=10, decimal_places=2, blank=True)),
                ('spouse_premium_per_month', models.DecimalField(null=True, verbose_name=b'calculated premium for spouse', max_digits=10, decimal_places=2, blank=True)),
                ('child_premium_per_month', models.DecimalField(null=True, verbose_name=b'calculated premium for child', max_digits=10, decimal_places=2, blank=True)),
                ('condition', models.CharField(max_length=64, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_supplemental_life_insurance_plan', models.ForeignKey(related_name='person_comp_suppl_life_insurance_plan', to='app.CompSupplLifeInsurancePlan')),
                ('person', models.ForeignKey(related_name='person_comp_suppl_life_insurance_plan', to='app.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplementalLifeInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupplementalLifeInsurancePlanRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age_min', models.SmallIntegerField(null=True, verbose_name=b'Min value of age. Null for children', blank=True)),
                ('age_max', models.SmallIntegerField(null=True, verbose_name=b'Max value of age. Null for children', blank=True)),
                ('bind_type', models.CharField(max_length=32, choices=[(b'self', b'Self'), (b'spouse', b'Spouse'), (b'dependent', b'Dependent')])),
                ('rate', models.DecimalField(max_digits=10, decimal_places=2)),
                ('condition', models.CharField(max_length=64, choices=[(b'tobacco', b'Tobacco'), (b'non-tobacco', b'Non-Tobacco')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('supplemental_life_insurance_plan', models.ForeignKey(related_name='supplemental_life_insurance_plan_rate', to='app.SupplementalLifeInsurancePlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='CompSupplLifeInsurancePlan',
            name='supplemental_life_insurance_plan',
            field=models.ForeignKey(related_name='comp_suppl_life_insurance_plan', to='app.SupplementalLifeInsurancePlan'),
            preserve_default=True,
        ),
    ]
