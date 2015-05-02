# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20150502_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyfsaplan',
            name='company',
            field=models.ForeignKey(related_name='company_fsa_plan_company', to='app.Company'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companyfsaplan',
            name='fsa_plan',
            field=models.ForeignKey(related_name='company_fsa_plan_fsa_plan', to='app.FsaPlan'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='job_title',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='person',
            field=models.ForeignKey(related_name='employee_profile_person', blank=True, to='app.Person', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsa',
            name='company_fsa_plan',
            field=models.ForeignKey(related_name='fsa_company_fsa_plan', to='app.CompanyFsaPlan', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsa',
            name='user',
            field=models.ForeignKey(related_name='fsa_user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsaplan',
            name='broker_user',
            field=models.ForeignKey(related_name='fsa_plan_broker', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='employeeprofile',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='employeeprofile',
            name='company',
        ),
    ]
