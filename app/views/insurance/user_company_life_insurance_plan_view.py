from rest_framework.views import APIView
from django.http import Http404

from rest_framework.response import Response

from rest_framework import status
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.serializers.insurance.user_company_life_insurance_serializer import (
    UserCompanyLifeInsuranceSerializer)
from app.models.company_user import CompanyUser


class UserCompanyBenefitPlanOptionView(APIView):
    """ single employee benefit """
    def _get_object(self, pk):
        try:
            return UserCompanyLifeInsurancePlan.objects.get(pk=pk)
        except UserCompanyLifeInsurancePlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = UserCompanyLifeInsurancePlan.objects.filter(user=pk)
        serializer = UserCompanyLifeInsuranceSerializer(plans, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = UserCompanyLifeInsuranceSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = UserCompanyLifeInsuranceSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyUsersLifeInsuranceView(APIView):
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
            return UserCompanyLifeInsurancePlan.objects.filter(user__in=users_id)
        except UserCompanyLifeInsurancePlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        users_id = self._get_users_id(pk)
        plans = self._get_objects(users_id)
        serializer = UserCompanyLifeInsuranceSerializer(plans, many=True)
        return Response(serializer.data)
