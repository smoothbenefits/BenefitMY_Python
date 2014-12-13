from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.company_user import CompanyUser
from app.serializers.company_user_serializer import (
    CompanyUserSerializer)
from view_mixin import *


class CompanyUserView(APIView, LoginRequiredMixin):
    def get_companies(self, pk):
        try:
            return CompanyUser.objects.filter(company=pk)
        except CompanyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        companies = self.get_companies(pk)
        serializer = CompanyUserSerializer(companies, many=True)
        return Response({'user_roles': serializer.data})


class CompanyEmployeeCountView(APIView, LoginRequiredMixin):

    def get(self, request, pk, format=None):
        return Response({'employees_count':
            len(CompanyUser.objects.filter(company=pk,
                                       company_user_type='employee'))})


class CompanyBrokerCountView(APIView, LoginRequiredMixin):

    def get(self, request, pk, format=None):
        return Response({'brokers_count':
            len(CompanyUser.objects.filter(company=pk,
                                       company_user_type='broker'))})


class BrokerCompanyCountView(APIView, LoginRequiredMixin):

    def get(self, request, pk, format=None):
        return Response({'companies_count':
            len(CompanyUser.objects.filter(user=pk,
                                       company_user_type='broker'))})
