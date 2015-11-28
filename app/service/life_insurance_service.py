import sys
from datetime import date
from django.http import Http404
from app.dtos.basic_life_insurance_cost import BasicLifeInsuranceCost
from app.service.compensation_service import CompensationService

class LifeInsuranceService(object):
    def __init__(self, life_insurance_plan):
        self._life_insurance_plan = life_insurance_plan

    def _use_fix_benefit_cost(self):
        if self._life_insurance_plan.total_cost_per_period and self._life_insurance_plan.employee_cost_per_period:
            return True

        if self._life_insurance_plan.total_cost_rate and self._life_insurance_plan.employee_contribution_percentage:
            return False

        return None

    def _get_effective_benefit_amount(self, insurance_amount, salary_multiplier, annual_salary):
        if insurance_amount:
            return int(insurance_amount)

        else:
            if not annual_salary:
                annual_salary = 0
            if not salary_multiplier:
                salary_multiplier = 0
            amount = salary_multiplier * annual_salary
            return amount

    def _get_total_premium(self, effective_benefit_amount, rate):
        total_premium = float(effective_benefit_amount * rate / 10)
        return total_premium

    def _get_employee_premium(self, total_premium, employee_contribution_percentage):
        if not total_premium:
            total_premium = 0
        employee_premium = 0
        if employee_contribution_percentage > 0:
            employee_premium = float(total_premium) *  float(employee_contribution_percentage) / 100
        return employee_premium


    def get_basic_life_insurance_cost_for_employee(self, personId):
        fix_cost = self._use_fix_benefit_cost()
        if fix_cost is None:
            raise ValueError('Company basic life insurance plan has incomplete cost data')

        compensation_service = CompensationService(personId)
        current_salary = compensation_service.get_current_annual_salary()
        benefit_amount = self._get_effective_benefit_amount(
            self._life_insurance_plan.insurance_amount,
            self._life_insurance_plan.salary_multiplier,
            current_salary
        )
        cost = None
        if fix_cost:
            cost = BasicLifeInsuranceCost(
                self._life_insurance_plan.total_cost_per_period,
                self._life_insurance_plan.employee_cost_per_period,
                benefit_amount
            )
        else:
            total_cost = self._get_total_premium(benefit_amount, self._life_insurance_plan.total_cost_rate)
            employee_cost = self._get_employee_premium(total_cost, self._life_insurance_plan.employee_contribution_percentage)
            cost = BasicLifeInsuranceCost(total_cost, employee_cost, benefit_amount)
        return cost
