# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_type', models.CharField(max_length=255, null=True)),
                ('street_1', models.CharField(max_length=255)),
                ('street_2', models.CharField(max_length=255, blank=True)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(default=b'AL', max_length=3, choices=[(b'AK', b'AK'), (b'AL', b'AL'), (b'AR', b'AR'), (b'AZ', b'AZ'), (b'CA', b'CA'), (b'CO', b'CO'), (b'CT', b'CT'), (b'DC', b'DC'), (b'DE', b'DE'), (b'FL', b'FL'), (b'GA', b'GA'), (b'HI', b'HI'), (b'IA', b'IA'), (b'ID', b'ID'), (b'IL', b'IL'), (b'IN', b'IN'), (b'KS', b'KS'), (b'KY', b'KY'), (b'LA', b'LA'), (b'MA', b'MA'), (b'MD', b'MD'), (b'ME', b'ME'), (b'MI', b'MI'), (b'MN', b'MN'), (b'MO', b'MO'), (b'MS', b'MS'), (b'MT', b'MT'), (b'NC', b'NC'), (b'ND', b'ND'), (b'NE', b'NE'), (b'NH', b'NH'), (b'NJ', b'NJ'), (b'NM', b'NM'), (b'NV', b'NV'), (b'NY', b'NY'), (b'OH', b'OH'), (b'OK', b'OK'), (b'OR', b'OR'), (b'PA', b'PA'), (b'PR', b'PR'), (b'RI', b'RI'), (b'SC', b'SC'), (b'SD', b'SD'), (b'TN', b'TN'), (b'TX', b'TX'), (b'UT', b'UT'), (b'VA', b'VA'), (b'VT', b'VT'), (b'WA', b'WA'), (b'WI', b'WI'), (b'WV', b'WV'), (b'WY', b'WY')])),
                ('zipcode', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BenefitPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BenefitType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, choices=[(b'Medical', b'Medical'), (b'Dental', b'Dental'), (b'Vision', b'Vision')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyBenefitPlanOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_cost_per_period', models.DecimalField(max_digits=20, decimal_places=2)),
                ('employee_cost_per_period', models.DecimalField(max_digits=20, decimal_places=2)),
                ('benefit_option_type', models.TextField(choices=[(b'individual', b'individual'), (b'individual_plus_spouse', b'individual_plus_spouse'), (b'individual_plus_child', b'individual_plus_child'), (b'individual_plus_one', b'individual_plus_one'), (b'individual_plus_children', b'individual_plus_children'), (b'family', b'family')])),
                ('benefit_plan', models.ForeignKey(related_name=b'company_benefit', blank=True, to='app.BenefitPlan', null=True)),
                ('company', models.ForeignKey(related_name=b'company_benefit', blank=True, to='app.Company', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_user_type', models.TextField(choices=[(b'Employee', b'Employee'), (b'Admin', b'Admin'), (b'Broker', b'Broker'), (b'Super', b'Super')])),
                ('company', models.ForeignKey(to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('edited', models.BooleanField(default=False)),
                ('company', models.ForeignKey(to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('value', models.TextField()),
                ('document', models.ForeignKey(related_name=b'document_field', to='app.Document')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Enrolled',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person_type', models.CharField(max_length=30)),
                ('full_name', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=255, null=True)),
                ('relationship', models.CharField(max_length=30, null=True)),
                ('ssn', models.CharField(max_length=30, null=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('company', models.ForeignKey(related_name=b'contacts', blank=True, to='app.Company', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_type', models.CharField(max_length=10)),
                ('number', models.CharField(max_length=32)),
                ('person', models.ForeignKey(related_name=b'phones', blank=True, to='app.Person', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('company', models.ForeignKey(related_name=b'template', to='app.Company')),
                ('document_type', models.ForeignKey(related_name=b'template', to='app.DocumentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCompanyBenefitPlanOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_benefit_plan_option', models.ForeignKey(related_name=b'user_company_benefit_plan', to='app.CompanyBenefitPlanOption')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='enrolled',
            name='person',
            field=models.ForeignKey(related_name=b'enrolled', to='app.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enrolled',
            name='user_company_benefit_plan_option',
            field=models.ForeignKey(related_name=b'enrolled', to='app.UserCompanyBenefitPlanOption'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='document_type',
            field=models.ForeignKey(blank=True, to='app.DocumentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='template',
            field=models.ForeignKey(blank=True, to='app.Template', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='benefitplan',
            name='btype',
            field=models.ForeignKey(related_name=b'benefit_plan', to='app.BenefitType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='company',
            field=models.ForeignKey(related_name=b'addresses', blank=True, to='app.Company', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='person',
            field=models.ForeignKey(related_name=b'addresses', blank=True, to='app.Person', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='companyuser',
            name='user',
            field=models.ForeignKey(to='app.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='user',
            field=models.ForeignKey(to='app.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.ForeignKey(related_name=b'person', blank=True, to='app.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanybenefitplanoption',
            name='user',
            field=models.ForeignKey(related_name=b'user_company_benefit_plan', to='app.User'),
            preserve_default=True,
        ),
    ]
