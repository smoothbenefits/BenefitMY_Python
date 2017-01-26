from rest_framework.views import APIView
from django.http import Http404

from rest_framework.response import Response

from rest_framework import status
from app.models.insurance.user_company_ltd_insurance_plan import \
    UserCompanyLtdInsurancePlan
from app.serializers.insurance.user_company_ltd_insurance_serializer import (
    UserCompanyLtdInsuranceSerializer, UserCompanyLtdInsurancePostSerializer)
from app.models.company_user import CompanyUser


class UserCompanyLtdInsuranceView(APIView):
    """ single employee benefit """
    def _get_object(self, pk):
        try:
            return UserCompanyLtdInsurancePlan.objects.get(pk=pk)
        except UserCompanyLtdInsurancePlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = UserCompanyLtdInsurancePlan.objects.filter(user=pk)
        serializer = UserCompanyLtdInsuranceSerializer(plans, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = UserCompanyLtdInsurancePostSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = UserCompanyLtdInsurancePostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyUsersLtdInsuranceView(APIView):
    """ benefit for all employees in a company """
    def _get_user_ids(self, pk):
        user_ids = []
        users = CompanyUser.objects.filter(company=pk,
                                           company_user_type='employee')
        for user in users:
            user_ids.append(user.user_id)
        return user_ids

    def _get_objects(self, user_ids):
        try:
            return UserCompanyLtdInsurancePlan.objects.filter(user__in=user_ids)
        except UserCompanyLtdInsurancePlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_ids = self._get_user_ids(pk)
        plans = self._get_objects(user_ids)
        serializer = UserCompanyLtdInsuranceSerializer(plans, many=True)
        return Response(serializer.data)
