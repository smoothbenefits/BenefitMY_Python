# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import encrypted_fields.fields
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

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
                ('company_user_type', models.TextField(choices=[(b'employee', b'employee'), (b'admin', b'admin'), (b'broker', b'broker'), (b'super', b'super')])),
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
                ('signature_type', models.CharField(max_length=10)),
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
                ('document_type', models.ForeignKey(related_name='template', to='app.DocumentType')),
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
                ('pcp', models.CharField(max_length=30, null=True, blank=True)),
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
            name='document_type',
            field=models.ForeignKey(blank=True, to='app.DocumentType', null=True),
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
    ]
