# test document
# tests can be kicked off by running "python manage.py test app/tests/"
from django.test import TestCase
from datetime import date
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

    def set_age_based_rates(self, rates):
        manager = MockRelationManager(rates)
        self.age_based_rates = manager

class MockRelationManager(object):

    def __init__(self, rates):
        self.rates = rates

    def all(self):
        return self.rates

class MockEmployeePerson(object):
    def __init__(self, birth_date):
        self.birth_date = birth_date

class MockAgeBasedRate(object):
    def __init__(self, age_min, age_max, rate):
        self.age_min = age_min
        self.age_max = age_max
        self.rate = rate

# Create your tests here.
class TestDisabilityInsuranceService(TestCase):
    def setUp(self):
        self.plan = MockCompanyPlan()
        self.person = MockEmployeePerson(date(1990, 1, 1))
        self.rates = []
        for i in range(10):
            lower = i * 5 + 20
            upper = (i + 1) * 5 + 20 - 1
            rate = MockAgeBasedRate(lower, upper, i + 1)
            self.rates.append(rate)

        self.rates.append(MockAgeBasedRate(None, 24, 0))
        self.rates.append(MockAgeBasedRate(70, None, 11))

        self.plan.set_age_based_rates(self.rates)
        self.disability_service = DisabilityInsuranceService(self.plan)

    def test_get_rate_succss(self):
        rate = self.disability_service.get_benefit_rate_of_cost(self.person)
        self.assertEqual(2, rate)

    def test_get_premium_success_monthly(self):
        effective = self.disability_service.get_effective_benefit_amount(23939, None, 12, 29937)
        self.assertEqual(effective, 1247)
        total = self.disability_service.get_total_premium(effective, self.plan.rate)
        employee = self.disability_service.get_employee_premium(total)
        self.assertEqual(employee, 22.13425)

    def test_get_premium_success_weekly(self):
        effective = self.disability_service.get_effective_benefit_amount(23939, None, 52, 29937)
        self.assertEqual(effective, 287)
        total = self.disability_service.get_total_premium(effective, self.plan.rate)
        employee = self.disability_service.get_employee_premium(total)
        self.assertEqual(employee, 5.09425)

    def test_get_total_premium_no_salary(self):
        total = self.disability_service.get_effective_benefit_amount(23939, None, 52, None)
        self.assertEqual(total, 0)

    def test_get_total_premium_no_max_benefit_amount(self):
        total = self.disability_service.get_effective_benefit_amount(0, None, 12, 32433)
        self.assertEqual(total, 0)
        total = self.disability_service.get_effective_benefit_amount(None, None, 12, 32433)
        self.assertEqual(total, 0)

    def test_get_total_premium_invalid_year_factor(self):
        self.assertRaises(ValueError, self.disability_service.get_effective_benefit_amount, 32444, None, None, 23414)

    def test_get_employee_premium_bad_total_premium(self):
        employee = self.disability_service.get_employee_premium(0)
        self.assertEqual(employee, 0)
        employee = self.disability_service.get_employee_premium(None)
        self.assertEqual(employee, 0)
