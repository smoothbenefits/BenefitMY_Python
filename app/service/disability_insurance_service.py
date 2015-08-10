
class DisabilityInsuranceService(object):
    def __init__(self, disability_plan):
        self._disability_plan = disability_plan

    def get_total_premium(self, max_benefit, year_factor, annual_salary):
        if not annual_salary:
            annual_salary = 0
        if not max_benefit:
            max_benefit = 0
        if not year_factor:
            raise ValueError('argument year_factor is invalid')
        unit_salary = annual_salary / year_factor
        benefit_from_salary = unit_salary * self._disability_plan.percentage_of_salary / 100
        max_benefit_amount = min(max_benefit, benefit_from_salary)
        total_premium = float(max_benefit_amount * self._disability_plan.rate / 10)
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