# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_sysbenefitupdatereasoncategory_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fsa',
            name='company_fsa_plan',
            field=models.ForeignKey(related_name='fsa_company_fsa_plan', blank=True, to='app.CompanyFsaPlan', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personcompsuppllifeinsuranceplan',
            name='company_supplemental_life_insurance_plan',
            field=models.ForeignKey(related_name='person_comp_suppl_life_insurance_plan', blank=True, to='app.CompSupplLifeInsurancePlan', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercompanylifeinsuranceplan',
            name='company_life_insurance',
            field=models.ForeignKey(related_name='life_insurance', blank=True, to='app.CompanyLifeInsurancePlan', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercompanyltdinsuranceplan',
            name='company_ltd_insurance',
            field=models.ForeignKey(related_name='ltd_insurance', blank=True, to='app.CompanyLtdInsurancePlan', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usercompanystdinsuranceplan',
            name='company_std_insurance',
            field=models.ForeignKey(related_name='std_insurance', blank=True, to='app.CompanyStdInsurancePlan', null=True),
            preserve_default=True,
        ),
    ]
