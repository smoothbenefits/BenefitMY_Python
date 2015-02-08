from rest_framework.views import APIView
from django.http import Http404

from rest_framework.response import Response

from django.db import transaction
from app.models.enrolled import Enrolled
from app.models.user_company_benefit_plan_option import UserCompanyBenefitPlanOption
from app.serializers.user_company_benefit_plan_option_serializer import (
    UserCompanyBenefitPlanOptionSerializer)
from app.models.company_user import CompanyUser


class BrokerUserBenefitOptionView(APIView):

    def _get_companies_by_broker_id(self, user_id):
        try:
            return CompanyUser.objects.filter(user=user_id,
                                              company_user_type='broker')
        except CompanyUser.DoesNotExist:
            raise Http401
    
    def _get_employees_by_company(self, company_id):
        employee_id_array = []
        employees = CompanyUser.objects.filter(company=company_id,
                                           company_user_type='employee')
        for employee in employees:
            employee_id_array.append(employee.user_id)
        return employee_id_array

    def _get_objects(self, users_id):
        try:
            return UserCompanyBenefitPlanOption.objects.filter(user__in=users_id)
        except UserCompanyBenefitPlanOption.DoesNotExist:
            raise Http404

    def get(self, request, broker_user_id, format=None):
        #with the user_id, get the actual companyuser
        broker_companies = self._get_companies_by_broker_id(broker_user_id)
        employee_array = []
        for broker_company in broker_companies:
            company_employees = self._get_employees_by_company(broker_company.company)
            employee_array.extend(company_employees)
        if employee_array:
            plans = self._get_objects(employee_array)
            serializer = UserCompanyBenefitPlanOptionSerializer(plans, many=True)
            return Response({'benefits': serializer.data})
        else:
            return Response({'benefits':[]})