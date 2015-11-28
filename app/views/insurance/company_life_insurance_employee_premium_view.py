from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.insurance.company_life_insurance_plan import \
    CompanyLifeInsurancePlan
from app.models.person import Person
from app.service.life_insurance_service import LifeInsuranceService

class CompanyLifeInsuranceEmployeePremiumView(APIView):
    def _get_plan(self, pk):
        try:
            return CompanyLifeInsurancePlan.objects.get(pk=pk)
        except CompanyLifeInsurancePlan.DoesNotExist:
            raise Http404

    def _get_employee_person(self, user_id):
        try:
            person_list = Person.objects.filter(user=user_id, relationship='self')
            if person_list:
                return person_list[0]
            return None
        except Person.DoesNotExist:
            return None

    def get(self, request, pk, user_id, format=None):
        company_plan = self._get_plan(pk)
        emp_person = self._get_employee_person(user_id)
        if not emp_person:
            return Response({'message': 'No Person Found'})

        life_insurance_service = LifeInsuranceService(company_plan)
        insurance_cost = life_insurance_service.get_basic_life_insurance_cost_for_employee(emp_person.id)
        return Response(
            {
                'total': insurance_cost.total_cost,
                'employee': insurance_cost.employee_cost,
                'amount': insurance_cost.benefit_amount
            }
        )
