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
    def test_get_premium_success(self):
        plan = MockCompanyPlan()
        disability_service = DisabilityInsuranceService(plan)
        total = disability_service.get_total_premium(23939, 29937)
        self.assertEqual(total, 62.35)
        employee = disability_service.get_employee_premium(total)
        self.assertEqual(employee, 22.13425)

    def test_get_total_premium_no_salary(self):
        plan = MockCompanyPlan()
        disability_service = DisabilityInsuranceService(plan)
        total = disability_service.get_total_premium(23939, None)
        self.assertEqual(total, 0)

    def test_get_total_premium_no_max_benefit_amount(self):
        plan = MockCompanyPlan()
        disability_service = DisabilityInsuranceService(plan)
        total = disability_service.get_total_premium(0, 32433)
        self.assertEqual(total, 0)
        total = disability_service.get_total_premium(None, 32433)
        self.assertEqual(total, 0)

    def test_get_employee_premium_bad_total_premium(self):
        plan = MockCompanyPlan()
        disability_service = DisabilityInsuranceService(plan)
        employee = disability_service.get_employee_premium(0)
        self.assertEqual(employee, 0)
        employee = disability_service.get_employee_premium(None)
        self.assertEqual(employee, 0)

