# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentAuthorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('worker_type', models.CharField(max_length=30, choices=[(b'Citizen', b'CItizen'), (b'Noncitizen', b'Noncitizen'), (b'PResident', b'PResideng'), (b'Aaw', b'Aaw')])),
                ('expiration_date', models.DateField()),
                ('uscis_number', models.CharField(max_length=255)),
                ('i_94', models.CharField(max_length=255, null=True, blank=True)),
                ('passport', models.CharField(max_length=255, null=True, blank=True)),
                ('country', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('signature', models.TextField()),
                ('signature_type', models.CharField(max_length=30, choices=[(b'step', b'step'), (b'final', b'final')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name=b'signature', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='W4',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('marriage', models.IntegerField()),
                ('dependencies', models.IntegerField()),
                ('head', models.IntegerField()),
                ('tax_credit', models.IntegerField()),
                ('total_points', models.IntegerField()),
                ('user', models.ForeignKey(related_name=b'w4', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='employmentauthorization',
            name='signature',
            field=models.ForeignKey(related_name=b'employment_authorization', blank=True, to='app.Signature', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employmentauthorization',
            name='user',
            field=models.ForeignKey(related_name=b'employment_authorization', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='benefitplan',
            old_name='btype',
            new_name='benefit_type',
        ),
        migrations.AddField(
            model_name='document',
            name='signature',
            field=models.ForeignKey(blank=True, to='app.Signature', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companyuser',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='document',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.ForeignKey(related_name=b'family', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='usercompanybenefitplanoption',
            name='user',
            field=models.ForeignKey(related_name=b'user_company_benefit_plan', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usercompanywaivedbenefit',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
