from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.insurance.company_std_insurance_plan import \
    CompanyStdInsurancePlan
from app.models.person import Person
from app.models.employee_compensation import EmployeeCompensation
from app.models.insurance.company_std_age_based_rate import CompanyStdAgeBasedRate
from app.service.disability_insurance_service import DisabilityInsuranceService
from app.service.compensation_service import CompensationService


class CompanyStdInsuranceEmployeePremiumView(APIView):
    def _get_plan(self, pk):
        try:
            return CompanyStdInsurancePlan.objects.get(pk=pk)
        except CompanyStdInsurancePlan.DoesNotExist:
            raise Http404

    def _get_employee_person(self, user_id):
        try:
            person_list = Person.objects.filter(user=user_id, relationship='self')
            if person_list:
                return person_list[0]
            return None
        except Person.DoesNotExist:
            return None

    def _get_plan_age_based_rates(self, plan_id):
        try:
            return CompanyStdAgeBasedRate.objects.filter(company_std_insurance_plan=plan_id)
        except CompanyStdAgeBasedRate.DoesNotExist:
            return None

    def get(self, request, pk, amount, user_id, format=None):
        std_plan = self._get_plan(pk)
        emp_person = self._get_employee_person(user_id)
        age_based_rates = self._get_plan_age_based_rates(pk)
        if not emp_person:
            return Response({'message': 'No Person Found'})
        compensation_service = CompensationService(emp_person.id)
        current_salary = None
        try:
            current_salary = compensation_service.get_current_annual_salary()
        except ValueError:
            return Response({'message':'No salary info'})
        disability_service = DisabilityInsuranceService(std_plan)
        effective_rate = disability_service.get_benefit_rate_of_cost(emp_person, age_based_rates)
        effective_benefit_amount = disability_service.get_effective_benefit_amount(
            std_plan.max_benefit_weekly, amount, 52, current_salary
        )
        total_premium = disability_service.get_total_premium(effective_benefit_amount, effective_rate)
        employee_premium = disability_service.get_employee_premium(total_premium)
        return Response(
            {
                'total': total_premium,
                'employee': employee_premium,
                'amount': effective_benefit_amount
            }
        )
