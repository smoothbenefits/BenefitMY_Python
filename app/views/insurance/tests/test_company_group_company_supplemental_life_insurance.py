import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views.tests.view_test_base import ViewTestBase

class CompanyGroupCompanySupplementalLifeInsuranceTestCase(TestCase, ViewTestBase):
    # your fixture files here
    fixtures = ['23_auth_user',
                '49_period_definition', '10_company',
                '34_company_user',
                '61_company_group',
                '26_supplemental_life_insurance',
                '39_company_supplement_life_insurance',
                '64_company_group_supplemental_life_insurance_plan']
    