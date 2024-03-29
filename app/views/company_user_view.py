import datetime

from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.person import Person
from app.models.company_user import CompanyUser
from app.models.employee_profile import EmployeeProfile
from app.serializers.company_user_serializer import (
    CompanyUserSerializer, CompanyUserDetailSerializer)
from app.service.company_personnel_service import CompanyPersonnelService


class CompanyUserView(APIView):
    def get_companies(self, pk):
        try:
            return CompanyUser.objects.filter(company=pk)
        except CompanyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        companies = self.get_companies(pk)
        serializer = CompanyUserSerializer(companies, many=True)
        return Response({'user_roles':serializer.data})


class CompanyEmployeeCountView(APIView):

    def get(self, request, pk, format=None):
        filter_status = request.QUERY_PARAMS.get('status', None)
        employees = CompanyUser.objects.select_related('user').filter(company=pk,
                                       company_user_type='employee')
        employee_count = len(employees)
        if filter_status:
            comp_personnel_service = CompanyPersonnelService()
            users_in_status = comp_personnel_service.get_company_employee_user_ids_with_status_in_time_range(
                pk,
                filter_status,
                datetime.date.today(),
                datetime.date.max)
            employee_count = len(users_in_status)

        return Response({'employees_count':
            employee_count})

class CompanyUserDetailView(APIView):

    def get(self, request, pk, role_type, format=None):
        try:
            companyUsers = CompanyUser.objects.filter(company=pk,
                                                      company_user_type=role_type)
            serializer = CompanyUserDetailSerializer(companyUsers, many=True)
            return Response({'company_broker': serializer.data})
        except CompanyUser.DoesNotExist:
            raise Http404

class CompanyBrokerCountView(APIView):

    def get(self, request, pk, format=None):
        return Response({'brokers_count':
            len(CompanyUser.objects.filter(company=pk,
                                       company_user_type='broker'))})

class BrokerCompanyCountView(APIView):

    def get(self, request, pk, format=None):
        return Response({'companies_count':
            len(CompanyUser.objects.filter(user=pk,
                                       company_user_type='broker'))})
