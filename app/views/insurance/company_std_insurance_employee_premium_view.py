from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.insurance.company_std_insurance_plan import \
    CompanyStdInsurancePlan
from app.models.person import Person
from app.models.employee_compensation import EmployeeCompensation
from app.service.disability_insurance_service import DisabilityInsuranceService


class CompanyStdInsuranceEmployeePremiumView(APIView):
    def _get_plan(self, pk):
        try:
            return CompanyStdInsurancePlan.objects.get(pk=pk)
        except CompanyStdInsurancePlan.DoesNotExist:
            raise Http404

    def _get_employee_compensation(self, user_id):
        try:
            person_list = Person.objects.filter(user=user_id, relationship='self')
            if person_list:
                person = person_list[0]
                empProfiles = EmployeeCompensation.objects.filter(person=person)
                if empProfiles:
                    return empProfiles[0]
            return None
        except Person.DoesNotExist:
            return None
        except EmployeeCompensation.DoesNotExist:
            return None

    def get(self, request, pk, user_id, format=None):
        emp_comp = self._get_employee_compensation(user_id)
        if not emp_comp or not emp_comp.annual_base_salary:
            return Response({'message':'No salary info'})
        std_plan = self._get_plan(pk)
        max_annual_benefit = std_plan.max_benefit_weekly * 52
        disability_service = DisabilityInsuranceService(std_plan)
        total_premium = disability_service.get_total_premium(max_annual_benefit, emp_comp.annual_base_salary)
        employee_premium = disability_service.get_employee_premium(total_premium)
        return Response({'total': total_premium, 'employee': employee_premium})