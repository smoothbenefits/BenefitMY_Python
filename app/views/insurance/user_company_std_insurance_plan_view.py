from rest_framework.views import APIView
from django.http import Http404

from rest_framework.response import Response

from rest_framework import status
from app.models.insurance.user_company_std_insurance_plan import \
    UserCompanyStdInsurancePlan
from app.serializers.insurance.user_company_std_insurance_serializer import (
    UserCompanyStdInsuranceSerializer, UserCompanyStdInsurancePostSerializer)
from app.models.company_user import CompanyUser


class UserCompanyStdInsuranceView(APIView):
    """ single employee benefit """
    def _get_object(self, pk):
        try:
            return UserCompanyStdInsurancePlan.objects.get(pk=pk)
        except UserCompanyStdInsurancePlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = UserCompanyStdInsurancePlan.objects.filter(user=pk)
        serializer = UserCompanyStdInsuranceSerializer(plans, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = UserCompanyStdInsurancePostSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = UserCompanyStdInsurancePostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyUsersStdInsuranceView(APIView):
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
            return UserCompanyStdInsurancePlan.objects.filter(user__in=user_ids)
        except UserCompanyStdInsurancePlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_ids = self._get_user_ids(pk)
        plans = self._get_objects(user_ids)
        serializer = UserCompanyStdInsuranceSerializer(plans, many=True)
        return Response(serializer.data)
