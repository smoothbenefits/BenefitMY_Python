# test document
# tests can be kicked off by running "python manage.py test app/tests/"
from django.test import TestCase
from app.service.disability_insurance_service import DisabilityInsuranceService

class MockCompanyPlan(object):
    class MockCompany(object):
        class MockPeriodDefinition(object):
            month_factor=0.5
        pay_period_definition = MockPeriodDefinition() 
    percentage_of_salary = 50
    rate = 0.5
    employer_contribution_percentage = 29
    company = MockCompany()


# Create your tests here.
class TestDisabilityInsuranceService(TestCase):
    def setUp(self):
        plan = MockCompanyPlan()
        self.disability_service = DisabilityInsuranceService(plan)
        
    def test_get_premium_success_monthly(self):
        total = self.disability_service.get_total_premium(23939, 12, 29937)
        self.assertEqual(total, 62.35)
        employee = self.disability_service.get_employee_premium(total)
        self.assertEqual(employee, 22.13425)

    def test_get_premium_success_weekly(self):
        total = self.disability_service.get_total_premium(23939, 52, 29937)
        self.assertEqual(total, 14.35)
        employee = self.disability_service.get_employee_premium(total)
        self.assertEqual(employee, 5.09425)

    def test_get_total_premium_no_salary(self):
        total = self.disability_service.get_total_premium(23939, 52, None)
        self.assertEqual(total, 0)

    def test_get_total_premium_no_max_benefit_amount(self):
        total = self.disability_service.get_total_premium(0, 12, 32433)
        self.assertEqual(total, 0)
        total = self.disability_service.get_total_premium(None, 12, 32433)
        self.assertEqual(total, 0)

    def test_get_total_premium_invalid_year_factor(self):
        self.assertRaises(ValueError, self.disability_service.get_total_premium, 32444, None, 23414)

    def test_get_employee_premium_bad_total_premium(self):
        employee = self.disability_service.get_employee_premium(0)
        self.assertEqual(employee, 0)
        employee = self.disability_service.get_employee_premium(None)
        self.assertEqual(employee, 0)

