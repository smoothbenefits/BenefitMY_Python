# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import encrypted_fields.fields
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.EmailField(db_index=True, unique=True, max_length=255, verbose_name=b'email address', validators=[django.core.validators.EmailValidator])),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
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
            name='BenefitDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=1024)),
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
            name='BenefitPolicyKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('rank', models.IntegerField(default=9999)),
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
                ('benefit_option_type', models.TextField(choices=[(b'individual', b'individual'), (b'individual_plus_spouse', b'individual_plus_spouse'), (b'individual_plus_family', b'individual_plus_family'), (b'individual_plus_children', b'individual_plus_children')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('benefit_plan', models.ForeignKey(related_name='company_benefit', blank=True, to='app.BenefitPlan', null=True)),
                ('company', models.ForeignKey(related_name='company_benefit', blank=True, to='app.Company', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyFeatures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_status', models.BooleanField(default=True)),
                ('company', models.ForeignKey(to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyLifeInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_cost_per_period', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('employee_cost_per_period', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('insurance_amount', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('salary_multiplier', models.IntegerField(null=True, blank=True)),
                ('benefit_option_type', models.TextField(blank=True, null=True, choices=[(b'individual', b'individual'), (b'individual_plus_spouse', b'individual_plus_spouse'), (b'individual_plus_family', b'individual_plus_family'), (b'individual_plus_children', b'individual_plus_children')])),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='company_life_insurance', blank=True, to='app.Company', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyLtdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('elimination_period_in_days', models.IntegerField(null=True, blank=True)),
                ('duration', models.IntegerField(null=True, blank=True)),
                ('percentage_of_salary', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('max_benefit_monthly', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='company_ltd_insurance', blank=True, to='app.Company', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyStdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('duration', models.IntegerField(null=True, blank=True)),
                ('percentage_of_salary', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('max_benefit_monthly', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='company_std_insurance', blank=True, to='app.Company', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_user_type', models.TextField(db_index=True, choices=[(b'employee', b'employee'), (b'admin', b'admin'), (b'broker', b'broker'), (b'super', b'super')])),
                ('new_employee', models.BooleanField(default=True)),
                ('company', models.ForeignKey(to='app.Company')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DirectDeposit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, null=True, max_digits=20, decimal_places=2, blank=True)),
                ('percentage', models.DecimalField(default=0, null=True, max_digits=5, decimal_places=2, blank=True)),
                ('remainder_of_all', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
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
                ('edited', models.BooleanField(default=False)),
                ('content', models.TextField(null=True, blank=True)),
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
                ('document', models.ForeignKey(related_name='fields', to='app.Document')),
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
                ('default_content', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('middle_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('relationship', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=32, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmploymentAuthorization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('worker_type', models.CharField(max_length=30, choices=[(b'Citizen', b'Citizen'), (b'Noncitizen', b'Noncitizen'), (b'PResident', b'PResident'), (b'Aaw', b'Aaw')])),
                ('expiration_date', models.DateField(null=True, blank=True)),
                ('uscis_number', models.CharField(max_length=255, null=True, blank=True)),
                ('i_94', models.CharField(max_length=255, null=True, blank=True)),
                ('passport', models.CharField(max_length=255, null=True, blank=True)),
                ('country', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Enrolled',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pcp', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FSA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('primary_amount_per_year', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('dependent_amount_per_year', models.DecimalField(null=True, max_digits=8, decimal_places=2)),
                ('update_reason', models.CharField(max_length=1024, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(related_name='fsa', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LifeInsuranceBeneficiary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('middle_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('relationship', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=32, null=True, blank=True)),
                ('percentage', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('tier', models.CharField(blank=True, max_length=1, null=True, choices=[(b'1', b'1'), (b'2', b'2')])),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LifeInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('attachment', models.CharField(max_length=2048, null=True, blank=True)),
                ('insurance_type', models.CharField(blank=True, max_length=16, null=True, choices=[(b'Basic', b'Basic'), (b'Extended', b'Extended')])),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(related_name='life_insurance_plan', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LtdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('attachment', models.CharField(max_length=2048, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(related_name='ltd_insurance_plan', to=settings.AUTH_USER_MODEL)),
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
                ('first_name', models.CharField(max_length=255, null=True)),
                ('middle_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('relationship', models.CharField(max_length=30, null=True)),
                ('ssn', encrypted_fields.fields.EncryptedTextField(null=True, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=2, null=True, choices=[(b'F', b'F'), (b'M', b'M')])),
                ('company', models.ForeignKey(related_name='contacts', blank=True, to='app.Company', null=True)),
                ('user', models.ForeignKey(related_name='family', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
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
                ('person', models.ForeignKey(related_name='phones', blank=True, to='app.Person', null=True)),
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
                ('signature_type', models.CharField(max_length=10, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='signature', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('attachment', models.CharField(max_length=2048, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(related_name='std_insurance_plan', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SysApplicationFeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature', models.CharField(max_length=32)),
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
                ('content', models.TextField(null=True, blank=True)),
                ('company', models.ForeignKey(related_name='template', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload_type', models.TextField(choices=[(b'I9', b'I9'), (b'Deposit', b'Deposit'), (b'Manager', b'Manager')])),
                ('S3', models.CharField(max_length=2048)),
                ('file_name', models.CharField(max_length=2048, null=True, blank=True)),
                ('file_type', models.CharField(max_length=128, null=True, blank=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('company', models.ForeignKey(related_name='company_upload', to='app.Company')),
                ('user', models.ForeignKey(related_name='user_upload', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserBankAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('routing', models.CharField(max_length=32)),
                ('account', models.CharField(max_length=32)),
                ('account_type', models.TextField(choices=[(b'Checking', b'Checking'), (b'Saving', b'Saving')])),
                ('bank_name', models.CharField(max_length=128, null=True, blank=True)),
                ('attachment', models.CharField(max_length=2048, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(related_name='user_bank_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCompanyBenefitPlanOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('benefit', models.ForeignKey(related_name='user_company_benefit_plan', to='app.CompanyBenefitPlanOption')),
                ('user', models.ForeignKey(related_name='user_company_benefit_plan', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCompanyLifeInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('insurance_amount', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_life_insurance', models.ForeignKey(related_name='life_insurance', to='app.CompanyLifeInsurancePlan')),
                ('person', models.ForeignKey(related_name='life_insurance', to='app.Person')),
                ('user', models.ForeignKey(related_name='user_company_life_insurance_plan', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCompanyLtdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_ltd_insurance', models.ForeignKey(related_name='ltd_insurance', to='app.CompanyLtdInsurancePlan')),
                ('user', models.ForeignKey(related_name='user_company_ltd_insurance_plan', to=settings.AUTH_USER_MODEL)),
                ('total_premium_per_period', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCompanyStdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_std_insurance', models.ForeignKey(related_name='std_insurance', to='app.CompanyStdInsurancePlan')),
                ('user', models.ForeignKey(related_name='user_company_std_insurance_plan', to=settings.AUTH_USER_MODEL)),
                ('total_premium_per_period', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserCompanyWaivedBenefit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reason', models.CharField(max_length=2048, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('benefit_type', models.ForeignKey(to='app.BenefitType')),
                ('company', models.ForeignKey(to='app.Company')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
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
                ('calculated_points', models.IntegerField()),
                ('user_defined_points', models.IntegerField(null=True, blank=True)),
                ('extra_amount', models.DecimalField(default=0, null=True, max_digits=20, decimal_places=2, blank=True)),
                ('user', models.ForeignKey(related_name='w4', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lifeinsurancebeneficiary',
            name='user_life_insurance_plan',
            field=models.ForeignKey(related_name='life_insurance_beneficiary', blank=True, to='app.UserCompanyLifeInsurancePlan', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enrolled',
            name='person',
            field=models.ForeignKey(related_name='enrolleds', to='app.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enrolled',
            name='user_company_benefit_plan_option',
            field=models.ForeignKey(related_name='enrolleds', to='app.UserCompanyBenefitPlanOption'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employmentauthorization',
            name='signature',
            field=models.ForeignKey(related_name='employment_authorization', blank=True, to='app.Signature', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employmentauthorization',
            name='user',
            field=models.ForeignKey(related_name='employment_authorization', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emergencycontact',
            name='person',
            field=models.ForeignKey(related_name='emergency_contact', blank=True, to='app.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='signature',
            field=models.ForeignKey(blank=True, to='app.Signature', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='directdeposit',
            name='bank_account',
            field=models.ForeignKey(related_name='direct_deposit', to='app.UserBankAccount'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='directdeposit',
            name='user',
            field=models.ForeignKey(related_name='direct_deposit', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='std_insurance_plan',
            field=models.ForeignKey(related_name='company_std_insurance', blank=True, to='app.StdInsurancePlan', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='ltd_insurance_plan',
            field=models.ForeignKey(related_name='company_ltd_insurance', blank=True, to='app.LtdInsurancePlan', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companylifeinsuranceplan',
            name='life_insurance_plan',
            field=models.ForeignKey(related_name='company_life_insurance', blank=True, to='app.LifeInsurancePlan', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyfeatures',
            name='company_feature',
            field=models.ForeignKey(to='app.SysApplicationFeature'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='benefitplan',
            name='benefit_type',
            field=models.ForeignKey(related_name='benefit_plan', to='app.BenefitType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='benefitdetails',
            name='benefit_plan',
            field=models.ForeignKey(related_name='benefit_details', blank=True, to='app.BenefitPlan', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='benefitdetails',
            name='benefit_policy_key',
            field=models.ForeignKey(related_name='benefit_details', blank=True, to='app.BenefitPolicyKey', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='benefitdetails',
            name='benefit_policy_type',
            field=models.ForeignKey(related_name='benefit_details', blank=True, to='app.BenefitPolicyType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='company',
            field=models.ForeignKey(related_name='addresses', blank=True, to='app.Company', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='person',
            field=models.ForeignKey(related_name='addresses', blank=True, to='app.Person', null=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='companystdinsuranceplan',
            old_name='max_benefit_monthly',
            new_name='max_benefit_weekly',
        ),
        migrations.CreateModel(
            name='UploadApplicationFeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_id', models.IntegerField()),
                ('application_feature', models.ForeignKey(related_name='upload_application_feature_app_feature', to='app.SysApplicationFeature')),
                ('upload', models.ForeignKey(related_name='upload_application_feature_upload', to='app.Upload')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_title', models.CharField(max_length=50, null=True)),
                ('annual_base_salary', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('employment_type', models.CharField(blank=True, max_length=30, null=True, choices=[(b'FullTime', b'FullTime'), (b'PartTime', b'PartTime'), (b'Contractor', b'Contractor'), (b'Intern', b'Intern')])),
                ('employment_status', models.CharField(blank=True, max_length=20, null=True, choices=[(b'Active', b'Active'), (b'Prospective', b'Prospective'), (b'Terminated', b'Terminated'), (b'OnLeave', b'OnLeave')])),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('person', models.ForeignKey(related_name='employee_profile_person', blank=True, to='app.Person', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='upload',
            name='upload_type',
        ),
        migrations.CreateModel(
            name='CompanyFsaPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FsaPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('broker_user', models.ForeignKey(related_name='fsa_plan_broker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companyfsaplan',
            name='fsa_plan',
            field=models.ForeignKey(related_name='company_fsa_plan_fsa_plan', to='app.FsaPlan'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fsa',
            name='company_fsa_plan',
            field=models.ForeignKey(related_name='fsa_company_fsa_plan', blank=True, to='app.CompanyFsaPlan', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsa',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 30, 13, 45, 1, 938000), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsa',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 30, 13, 45, 1, 938000), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsa',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsa',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='company',
            field=models.ForeignKey(related_name='employee_profile_company', default=0, to='app.Company'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='job_title',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='person',
            field=models.ForeignKey(related_name='employee_profile_person', default=0, to='app.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime.now, auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='employeeprofile',
            unique_together=set([('person', 'company')]),
        ),
        migrations.AlterField(
            model_name='companyfsaplan',
            name='company',
            field=models.ForeignKey(related_name='company_fsa_plan_company', to='app.Company'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsa',
            name='user',
            field=models.ForeignKey(related_name='fsa_user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='companyltdinsuranceplan',
            old_name='elimination_period_in_days',
            new_name='elimination_period_in_months',
        ),
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='paid_by',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'Employee', b'Employee'), (b'Employer', b'Employer')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='rate',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='elimination_period_in_days',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='paid_by',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'Employee', b'Employee'), (b'Employer', b'Employer')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='rate',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='relationship',
            field=models.CharField(default=b'dependent', max_length=30, choices=[(b'self', b'self'), (b'dependent', b'dependent'), (b'spouse', b'spouse')]),
            preserve_default=True,
        ),
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
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('supplemental_life_insurance_plan', models.ForeignKey(related_name='supplemental_life_insurance_plan_rate', blank=True, to='app.SupplementalLifeInsurancePlan', null=True)),
                ('benefit_reduction_percentage', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
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
        migrations.CreateModel(
            name='SupplementalLifeInsuranceBeneficiary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255, null=True)),
                ('middle_name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('relationship', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=32, null=True, blank=True)),
                ('percentage', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('tier', models.CharField(blank=True, max_length=1, null=True, choices=[(b'1', b'1'), (b'2', b'2')])),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('person_comp_suppl_life_insurance_plan', models.ForeignKey(related_name='suppl_life_insurance_beneficiary', blank=True, to='app.PersonCompSupplLifeInsurancePlan', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SysSupplLifeInsuranceCondition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='personcompsuppllifeinsuranceplan',
            name='condition',
        ),
        migrations.AddField(
            model_name='supplementallifeinsuranceplanrate',
            name='condition',
            field=models.ForeignKey(related_name='supplemental_life_insurance_plan_rate', default=1, to='app.SysSupplLifeInsuranceCondition'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='self_condition',
            field=models.ForeignKey(related_name='person_comp_suppl_life_insurance_plan_self', blank=True, to='app.SysSupplLifeInsuranceCondition', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='spouse_condition',
            field=models.ForeignKey(related_name='person_comp_suppl_life_insurance_plan_spouse', blank=True, to='app.SysSupplLifeInsuranceCondition', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='supplementallifeinsuranceplan',
            name='use_employee_age_for_spouse',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='employer_contribution_percentage',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='employer_contribution_percentage',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='CompanyHraPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='company_hra_plan', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HraPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=2048, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonCompanyHraPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_hra_plan', models.ForeignKey(related_name='person_company_hra_plan', to='app.CompanyHraPlan')),
                ('person', models.ForeignKey(related_name='person_company_hra_plan', to='app.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companyhraplan',
            name='hra_plan',
            field=models.ForeignKey(related_name='company_hra_plan', to='app.HraPlan'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companybenefitplanoption',
            name='benefit_option_type',
            field=models.TextField(choices=[(b'individual', b'individual'), (b'individual_plus_spouse', b'individual_plus_spouse'), (b'individual_plus_family', b'individual_plus_family'), (b'individual_plus_children', b'individual_plus_children'), (b'individual_plus_one', b'individual_plus_one')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='benefitplan',
            name='mandatory_pcp',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='benefitplan',
            name='pcp_link',
            field=models.CharField(max_length=2048, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='SysBenefitUpdateReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fsa',
            name='record_reason',
            field=models.ForeignKey(related_name='fsa_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fsa',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompanyhraplan',
            name='record_reason',
            field=models.ForeignKey(related_name='hra_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompanyhraplan',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='record_reason',
            field=models.ForeignKey(related_name='suppl_life_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanybenefitplanoption',
            name='record_reason',
            field=models.ForeignKey(related_name='health_benefit_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanybenefitplanoption',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanylifeinsuranceplan',
            name='record_reason',
            field=models.ForeignKey(related_name='basic_life_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanylifeinsuranceplan',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanyltdinsuranceplan',
            name='record_reason',
            field=models.ForeignKey(related_name='ltd_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanyltdinsuranceplan',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanystdinsuranceplan',
            name='record_reason',
            field=models.ForeignKey(related_name='std_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanystdinsuranceplan',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanywaivedbenefit',
            name='record_reason',
            field=models.ForeignKey(related_name='health_benefit_waive_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanywaivedbenefit',
            name='record_reason_note',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='reason_for_change',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='SysBenefitUpdateReasonCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
                ('rank', models.PositiveSmallIntegerField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sysbenefitupdatereason',
            name='category',
            field=models.ForeignKey(related_name='benefit_update_reason_category', blank=True, to='app.SysBenefitUpdateReasonCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sysbenefitupdatereason',
            name='detail_required',
            field=models.BooleanField(default=False),
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
        migrations.AlterField(
            model_name='fsa',
            name='dependent_amount_per_year',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fsa',
            name='primary_amount_per_year',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='SysPeriodDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('month_factor', models.FloatField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='company',
            name='pay_period_definition',
            field=models.ForeignKey(related_name='sys_pay_period_definition', default=2, to='app.SysPeriodDefinition'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companybenefitplanoption',
            name='employee_cost_per_period',
            field=models.DecimalField(max_digits=20, decimal_places=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='companylifeinsuranceplan',
            name='employee_cost_per_period',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personcompsuppllifeinsuranceplan',
            name='child_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated premium for child', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personcompsuppllifeinsuranceplan',
            name='self_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated premium for self', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='personcompsuppllifeinsuranceplan',
            name='spouse_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated premium for spouse', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='usercompanyltdinsuranceplan',
            old_name='total_premium_per_period',
            new_name='total_premium_per_month',
        ),
        migrations.AlterField(
            model_name='usercompanyltdinsuranceplan',
            name='total_premium_per_month',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='usercompanystdinsuranceplan',
            old_name='total_premium_per_period',
            new_name='total_premium_per_month',
        ),
        migrations.AlterField(
            model_name='usercompanystdinsuranceplan',
            name='total_premium_per_month',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='relationship',
            field=models.CharField(default=b'dependent', max_length=30, choices=[(b'self', b'self'), (b'dependent', b'dependent'), (b'spouse', b'spouse'), (b'child', b'child'), (b'life partner', b'life partner'), (b'ex spouse', b'ex spouse'), (b'disabled dependent', b'disabled dependent'), (b'step child', b'step child')]),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='EmployeeCompensation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('annual_base_salary', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('increase_percentage', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('effective_date', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, auto_now=True)),
                ('company', models.ForeignKey(related_name='employee_compensation_company', blank=True, to='app.Company', null=True)),
                ('person', models.ForeignKey(related_name='employee_compensation_person', blank=True, to='app.Person', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SysCompensationUpdateReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('created_at', models.DateField(default=datetime.datetime.now, auto_now_add=True)),
                ('updated_at', models.DateField(default=datetime.datetime.now, auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='employeecompensation',
            name='reason',
            field=models.ForeignKey(related_name='employee_compensation', blank=True, to='app.SysCompensationUpdateReason', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='relationship',
            field=models.CharField(default=b'dependent', max_length=30, choices=[(b'self', b'self'), (b'dependent', b'dependent'), (b'spouse', b'spouse'), (b'child', b'child'), (b'life partner', b'life partner'), (b'ex-spouse', b'ex-spouse'), (b'disabled dependent', b'disabled dependent'), (b'stepchild', b'stepchild')]),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='EmployeeTimeTracking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actual_hour_month', models.DateField()),
                ('actual_hour_per_month', models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, auto_now=True)),
                ('company', models.ForeignKey(related_name='employee_timetracking_company', to='app.Company')),
                ('person', models.ForeignKey(related_name='employee_timetracking_person', to='app.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='employeetimetracking',
            unique_together=set([('person', 'company')]),
        ),
        migrations.AddField(
            model_name='employeecompensation',
            name='hourly_rate',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeecompensation',
            name='projected_hour_per_month',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='pay_rate',
            field=models.ForeignKey(related_name='employee_profile_pay_rate', blank=True, to='app.SysPeriodDefinition', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='ein',
            field=models.CharField(max_length=30, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='offer_of_coverage_code',
            field=models.CharField(max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Company1095C',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('offer_of_coverage', models.CharField(max_length=2, null=True, blank=True)),
                ('employee_share', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('safe_harbor', models.CharField(max_length=10, null=True, blank=True)),
                ('period', models.CharField(default=b'All 12 Months', max_length=14, choices=[(b'All 12 Months', b'All 12 Months'), (b'Jan', b'Jan'), (b'Feb', b'Feb'), (b'Mar', b'Mar'), (b'Apr', b'Apr'), (b'May', b'May'), (b'June', b'June'), (b'July', b'July'), (b'Aug', b'Aug'), (b'Sept', b'Sept'), (b'Oct', b'Oct'), (b'Nov', b'Nov'), (b'Dec', b'Dec')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(related_name='company_1095C', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyLtdAgeBasedRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age_min', models.SmallIntegerField(null=True, verbose_name=b'Min value of age.', blank=True)),
                ('age_max', models.SmallIntegerField(null=True, verbose_name=b'Max value of age.', blank=True)),
                ('rate', models.DecimalField(max_digits=20, decimal_places=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_ltd_insurance_plan', models.ForeignKey(related_name='age_based_rates', to='app.CompanyLtdInsurancePlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyStdAgeBasedRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age_min', models.SmallIntegerField(null=True, verbose_name=b'Min value of age.', blank=True)),
                ('age_max', models.SmallIntegerField(null=True, verbose_name=b'Max value of age.', blank=True)),
                ('rate', models.DecimalField(max_digits=20, decimal_places=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_std_insurance_plan', models.ForeignKey(related_name='age_based_rates', to='app.CompanyStdInsurancePlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='benefit_amount_step',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companyltdinsuranceplan',
            name='user_amount_required',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='benefit_amount_step',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companystdinsuranceplan',
            name='user_amount_required',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanyltdinsuranceplan',
            name='user_select_amount',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usercompanystdinsuranceplan',
            name='user_select_amount',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='child_adad_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated adad premium for child', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='self_adad_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated adad premium for self', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='personcompsuppllifeinsuranceplan',
            name='spouse_adad_premium_per_month',
            field=models.DecimalField(null=True, verbose_name=b'calculated adad premium for spouse', max_digits=22, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='CompanyCommuterPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan_name', models.CharField(max_length=255, null=True, blank=True)),
                ('enable_transit_benefit', models.BooleanField(default=False)),
                ('enable_parking_benefit', models.BooleanField(default=False)),
                ('employer_transit_contribution', models.DecimalField(max_digits=20, decimal_places=10)),
                ('employer_parking_contribution', models.DecimalField(max_digits=20, decimal_places=10)),
                ('deduction_period', models.CharField(max_length=30, choices=[(b'Monthly', b'Monthly'), (b'PerPayPeriod', b'PerPayPeriod')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='company_commuter_plan', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonCompanyCommuterPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monthly_amount_transit_pre_tax', models.DecimalField(max_digits=20, decimal_places=10)),
                ('monthly_amount_transit_post_tax', models.DecimalField(max_digits=20, decimal_places=10)),
                ('monthly_amount_parking_pre_tax', models.DecimalField(max_digits=20, decimal_places=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_commuter_plan', models.ForeignKey(related_name='person_company_commuter_plan', to='app.CompanyCommuterPlan')),
                ('person', models.ForeignKey(related_name='person_company_commuter_plan', to='app.Person')),
                ('monthly_amount_parking_post_tax', models.DecimalField(max_digits=20, decimal_places=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='employment_type',
            field=models.CharField(blank=True, max_length=30, null=True, choices=[(b'FullTime', b'FullTime'), (b'PartTime', b'PartTime'), (b'Contractor', b'Contractor'), (b'Intern', b'Intern'), (b'PerDiem', b'PerDiem')]),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Employee1095C',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('safe_harbor', models.CharField(max_length=10, null=True, blank=True)),
                ('period', models.CharField(default=b'All 12 Months', max_length=14, choices=[(b'All 12 Months', b'All 12 Months'), (b'Jan', b'Jan'), (b'Feb', b'Feb'), (b'Mar', b'Mar'), (b'Apr', b'Apr'), (b'May', b'May'), (b'June', b'June'), (b'July', b'July'), (b'Aug', b'Aug'), (b'Sept', b'Sept'), (b'Oct', b'Oct'), (b'Nov', b'Nov'), (b'Dec', b'Dec')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='employee_aca_profile_company', to='app.Company')),
                ('person', models.ForeignKey(related_name='employee_aca_profile_person', to='app.Person')),
                ('employee_share', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('offer_of_coverage', models.CharField(max_length=2, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='benefit_start_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='CompanyExtraBenefitPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=4000, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='company_extra_benefit_plan', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtraBenefitItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_plan', models.ForeignKey(related_name='benefit_items', blank=True, to='app.CompanyExtraBenefitPlan', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonCompanyExtraBenefitPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('record_reason_note', models.CharField(max_length=512, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_plan', models.ForeignKey(related_name='person_company_extra_benefit_plan', to='app.CompanyExtraBenefitPlan')),
                ('person', models.ForeignKey(related_name='person_company_extra_benefit_plan', to='app.Person')),
                ('record_reason', models.ForeignKey(related_name='extra_benefits_update_reason', blank=True, to='app.SysBenefitUpdateReason', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonCompanyExtraBenefitPlanItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opt_in', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('extra_benefit_item', models.ForeignKey(related_name='person_company_extra_benefit_plans', to='app.ExtraBenefitItem')),
                ('person_company_extra_benefit_plan', models.ForeignKey(related_name='plan_items', blank=True, to='app.PersonCompanyExtraBenefitPlan', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company1094CMemberInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_of_1095c', models.PositiveIntegerField(default=0)),
                ('authoritative_transmittal', models.BooleanField(default=False)),
                ('member_of_aggregated_group', models.BooleanField(default=False)),
                ('certifications_of_eligibility', models.CharField(default=b'Qualifying Offer Method', max_length=50, choices=[(b'Qualifying Offer Method', b'Qualifying Offer Method'), (b'Qualifying Offer Method Transition Relief', b'Qualifying Offer Method Transition Relief'), (b'Section 4980H Transition Relief', b'Section 4980H Transition Relief'), (b'98 Percent Offer Method', b'98 Percent Offer Method')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='company_1094C', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company1094CMonthlyMemberInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minimum_essential_coverage', models.BooleanField(default=False)),
                ('fulltime_employee_count', models.PositiveIntegerField(default=0)),
                ('total_employee_count', models.PositiveIntegerField(default=0)),
                ('aggregated_group', models.BooleanField(default=False)),
                ('section_4980h_transition_relief', models.CharField(default=b'', max_length=2)),
                ('period', models.CharField(default=b'All 12 Months', max_length=14, choices=[(b'All 12 Months', b'All 12 Months'), (b'Jan', b'Jan'), (b'Feb', b'Feb'), (b'Mar', b'Mar'), (b'Apr', b'Apr'), (b'May', b'May'), (b'June', b'June'), (b'July', b'July'), (b'Aug', b'Aug'), (b'Sept', b'Sept'), (b'Oct', b'Oct'), (b'Nov', b'Nov'), (b'Dec', b'Dec')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='company_1094C_monthly', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='personcompanyhraplan',
            name='company_hra_plan',
            field=models.ForeignKey(related_name='person_company_hra_plan', blank=True, to='app.CompanyHraPlan', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='upload',
            field=models.ForeignKey(related_name='document_uploads', blank=True, to='app.Upload', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='template',
            name='upload',
            field=models.ForeignKey(related_name='template_uploads', blank=True, to='app.Upload', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companylifeinsuranceplan',
            name='employee_contribution_percentage',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companylifeinsuranceplan',
            name='total_cost_rate',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='CompanyGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyGroupMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('company_group', models.ForeignKey(related_name='company_group_members', to='app.CompanyGroup')),
                ('user', models.ForeignKey(related_name='company_group_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyGroupBasicLifeInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_basic_life_insurance_plan', models.ForeignKey(related_name='company_group_basic_life_insurance', to='app.CompanyLifeInsurancePlan')),
                ('company_group', models.ForeignKey(related_name='basic_life_insurance_plan', to='app.CompanyGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyGroupSupplLifeInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_group', models.ForeignKey(related_name='suppl_life_insurance_plan', to='app.CompanyGroup')),
                ('company_suppl_life_insurance_plan', models.ForeignKey(related_name='company_group_suppl_life_insurance', to='app.CompSupplLifeInsurancePlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
                ('company_hsa_plan', models.ForeignKey(related_name='person_hsa_selection', blank=True, to='app.CompanyHsaPlan', null=True)),
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
        migrations.AlterField(
            model_name='companygrouphsaplan',
            name='company_group',
            field=models.ForeignKey(related_name='company_hsa_plan', to='app.CompanyGroup'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='CompanyGroupBenefitPlanOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_benefit_plan_option', models.ForeignKey(related_name='company_group_benefit_plan_option', to='app.CompanyBenefitPlanOption')),
                ('company_group', models.ForeignKey(related_name='health_benefit_plan_option', to='app.CompanyGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyGroupStdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_group', models.ForeignKey(related_name='company_std_insurance_plan', to='app.CompanyGroup')),
                ('company_std_insurance_plan', models.ForeignKey(related_name='company_group_std', to='app.CompanyStdInsurancePlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyGroupHraPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_group', models.ForeignKey(related_name='hra_plan', to='app.CompanyGroup')),
                ('company_hra_plan', models.ForeignKey(related_name='company_group_hra', to='app.CompanyHraPlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyGroupLtdInsurancePlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_group', models.ForeignKey(related_name='company_ltd_insurance_plan', to='app.CompanyGroup')),
                ('company_ltd_insurance_plan', models.ForeignKey(related_name='company_group_ltd', to='app.CompanyLtdInsurancePlan')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyGroupFsaPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_fsa_plan', models.ForeignKey(related_name='company_group_fsa', to='app.CompanyFsaPlan')),
                ('company_group', models.ForeignKey(related_name='fsa_plan', to='app.CompanyGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyGroupCommuterPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_commuter_plan', models.ForeignKey(related_name='company_group_commuter', to='app.CompanyCommuterPlan')),
                ('company_group', models.ForeignKey(related_name='commuter_plan', to='app.CompanyGroup')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='manager',
            field=models.ForeignKey(related_name='direct_reports', blank=True, to='app.EmployeeProfile', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='UserOnboardingStepState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('step', models.CharField(max_length=255, choices=[(b'direct_deposit', b'direct_deposit')])),
                ('state', models.CharField(blank=True, max_length=2048, null=True, choices=[(b'skipped', b'skipped'), (b'completed', b'completed')])),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='onboarding_step_state', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='useronboardingstepstate',
            unique_together=set([('step', 'user')]),
        ),
        migrations.CreateModel(
            name='EmailBlockList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_block_feature', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='email_block_feature', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyServiceProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider_type', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=1024)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=32, null=True, blank=True)),
                ('link', models.CharField(max_length=1024, null=True, blank=True)),
                ('show_to_employee', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='service_provider', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CompanyPhraseology',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1024)),
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
        migrations.AlterField(
            model_name='employeephraseology',
            name='end_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employeephraseology',
            name='start_date',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='person_type',
            field=models.CharField(max_length=30, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='relationship',
            field=models.CharField(default=b'dependent', max_length=30, db_index=True, choices=[(b'self', b'self'), (b'dependent', b'dependent'), (b'spouse', b'spouse'), (b'child', b'child'), (b'life partner', b'life partner'), (b'ex-spouse', b'ex-spouse'), (b'disabled dependent', b'disabled dependent'), (b'stepchild', b'stepchild')]),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='UploadForUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upload', models.ForeignKey(related_name='upload_for_user_upload', to='app.Upload')),
                ('user_for', models.ForeignKey(related_name='upload_for_user_user_for', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OpenEnrollmentDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_month', models.IntegerField()),
                ('start_day', models.IntegerField()),
                ('end_month', models.IntegerField()),
                ('end_day', models.IntegerField()),
                ('company', models.ForeignKey(related_name='employment_authorization', to='app.Company', unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='employeeprofile',
            name='employment_status',
            field=models.CharField(default=b'Active', max_length=20, choices=[(b'Active', b'Active'), (b'Prospective', b'Prospective'), (b'Terminated', b'Terminated'), (b'OnLeave', b'OnLeave')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='employee_number',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='employeeprofile',
            unique_together=set([('person', 'company'), ('employee_number', 'company')]),
        ),
        migrations.CreateModel(
            name='CompanyIntegrationProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_external_id', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(related_name='integration_provider', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IntegrationProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('service_type', models.CharField(max_length=30, choices=[(b'Payroll', b'Payroll')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='integrationprovider',
            unique_together=set([('name', 'service_type')]),
        ),
        migrations.AddField(
            model_name='companyintegrationprovider',
            name='integration_provider',
            field=models.ForeignKey(related_name='company_list', to='app.IntegrationProvider'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='companyintegrationprovider',
            unique_together=set([('company', 'integration_provider'), ('company_external_id', 'integration_provider')]),
        ),
        migrations.CreateModel(
            name='CompanyDepartment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('company', models.ForeignKey(related_name='company_company_department', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='companydepartment',
            unique_together=set([('company', 'department')]),
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='department',
            field=models.ForeignKey(related_name='employee_profile_company_department', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='app.CompanyDepartment', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='CompanyUserIntegrationProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_user_external_id', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company_user', models.ForeignKey(related_name='integration_provider', to='app.CompanyUser')),
                ('integration_provider', models.ForeignKey(related_name='company_user_list', to='app.IntegrationProvider')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='companyuserintegrationprovider',
            unique_together=set([('company_user', 'integration_provider'), ('company_user_external_id', 'integration_provider')]),
        ),
        migrations.CreateModel(
            name='SystemSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=127)),
                ('value', models.CharField(max_length=1023, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='companyintegrationprovider',
            name='employee_external_id_seed',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='photo_url',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeeprofile',
            name='pin',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='employeeprofile',
            unique_together=set([('person', 'company'), ('pin', 'company'), ('employee_number', 'company')]),
        ),
        migrations.CreateModel(
            name='CompanyUserFeatures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_status', models.BooleanField(default=True)),
                ('company_user', models.ForeignKey(to='app.CompanyUser')),
                ('feature', models.ForeignKey(to='app.SysApplicationFeature')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='companyuserintegrationprovider',
            unique_together=set([('company_user', 'integration_provider')]),
        ),
    ]
