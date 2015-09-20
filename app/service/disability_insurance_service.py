import sys
from datetime import date
from django.http import Http404
from app.models.person import Person

class DisabilityInsuranceService(object):
    def __init__(self, disability_plan):
        self._disability_plan = disability_plan

    def _get_user_age(self, person):
        # Copied shamelessly from Stackoverflow
        today = date.today()
        born = person.birth_date

        if not born:
            raise ValueError('Could not find the birth date of the employee')

        age = today.year - born.year
        if (born.month > today.month):
            age = age - 1
        elif (born.month == today.month and born.day > today.day):
            age = age - 1
        return age

    def get_benefit_rate_of_cost(self, person):
        age_based_rates = self._disability_plan.age_based_rates.all()
        if not age_based_rates:
            return self._disability_plan.rate

        age = self._get_user_age(person)
        for rate in age_based_rates:
            if not rate.age_min:
                rate.age_min = 0
            if not rate.age_max:
                rate.age_max = 1000 # Use a large number as max age if not provided
            if rate.age_min <= age and rate.age_max >= age:
                return rate.rate

        raise ValueError('Could not find a rate for the emplyee')

    def get_effective_benefit_amount(self, max_benefit, selected_amount,
                                     year_factor, annual_salary):
        if not annual_salary:
            annual_salary = 0
        if not max_benefit:
            max_benefit = 0
        if not year_factor:
            raise ValueError('argument year_factor is invalid')
        if not selected_amount:
            selected_amount = sys.maxint
        else:
            selected_amount = int(selected_amount)
        unit_salary = annual_salary / year_factor
        benefit_from_salary = unit_salary * self._disability_plan.percentage_of_salary / 100
        return min(max_benefit, benefit_from_salary, selected_amount)

    def get_total_premium(self, effective_benefit_amount, rate):
        total_premium = float(effective_benefit_amount * rate / 10)
        return total_premium

    def get_employee_premium(self, total_premium):
        if not total_premium:
            total_premium = 0
        employee_contribution_percent = 100
        if self._disability_plan.employer_contribution_percentage:
            employee_contribution_percent = 100 - self._disability_plan.employer_contribution_percentage
        employee_premium = 0
        if employee_contribution_percent > 0:
            employee_premium = float(total_premium) *  float(employee_contribution_percent) / 100 * self._disability_plan.company.pay_period_definition.month_factor
        return employee_premium
