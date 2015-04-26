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
    def _get_users_id(self, pk):
        users_id = []
        users = CompanyUser.objects.filter(company=pk,
                                           company_user_type='employee')
        for user in users:
            users_id.append(user.user_id)
        return users_id

    def _get_objects(self, users_id):
        try:
            return UserCompanyStdInsurancePlan.objects.filter(user__in=users_id)
        except UserCompanyStdInsurancePlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        users_id = self._get_users_id(pk)
        plans = self._get_objects(users_id)
        serializer = UserCompanyStdInsuranceSerializer(plans, many=True)
        return Response(serializer.data)
