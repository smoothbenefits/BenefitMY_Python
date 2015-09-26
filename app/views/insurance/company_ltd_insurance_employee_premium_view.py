from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.insurance.company_ltd_insurance_plan import \
    CompanyLtdInsurancePlan
from app.models.person import Person
from app.models.employee_compensation import EmployeeCompensation
from app.models.insurance.company_ltd_age_based_rate import CompanyLtdAgeBasedRate
from app.service.disability_insurance_service import DisabilityInsuranceService
from app.service.compensation_service import CompensationService


class CompanyLtdInsuranceEmployeePremiumView(APIView):
    def _get_plan(self, pk):
        try:
            return CompanyLtdInsurancePlan.objects.get(pk=pk)
        except CompanyLtdInsurancePlan.DoesNotExist:
            raise Http404

    def _get_employee_person(self, user_id):
        try:
            person_list = Person.objects.filter(user=user_id, relationship='self')
            if person_list:
                return person_list[0]
            return None
        except Person.DoesNotExist:
            return None

    def post(self, request, pk, user_id, format=None):
        ltd_plan = self._get_plan(pk)
        emp_person = self._get_employee_person(user_id)
        if not emp_person:
            return Response({'message': 'No Person Found'})
        compensation_service = CompensationService(emp_person.id)
        current_salary = None
        try:
            current_salary = compensation_service.get_current_annual_salary()
        except ValueError:
            return Response({'message':'No salary info'})

        if not request.DATA['amount'] and request.DATA['amount'] != 0:
            amount = None
        else:
            amount = request.DATA['amount']

        disability_service = DisabilityInsuranceService(ltd_plan)
        effective_rate = disability_service.get_benefit_rate_of_cost(emp_person)
        effective_benefit_amount = disability_service.get_effective_benefit_amount(
            ltd_plan.max_benefit_monthly, amount, 12, current_salary
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
