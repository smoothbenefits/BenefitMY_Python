from rest_framework.views import APIView
from django.http import Http404

from rest_framework.response import Response

from rest_framework import status
from app.models.insurance.user_company_life_insurance_plan import \
    UserCompanyLifeInsurancePlan
from app.serializers.insurance.user_company_life_insurance_serializer import (
    UserCompanyLifeInsuranceSerializer, UserCompanyLifeInsurancePostSerializer)
from app.models.company_user import CompanyUser


class UserCompanyLifeInsuranceView(APIView):
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
        serializer = UserCompanyLifeInsurancePostSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = UserCompanyLifeInsurancePostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyUsersLifeInsuranceView(APIView):
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
            return UserCompanyLifeInsurancePlan.objects.filter(user__in=user_ids)
        except UserCompanyLifeInsurancePlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user_ids = self._get_user_ids(pk)
        plans = self._get_objects(user_ids)
        serializer = UserCompanyLifeInsuranceSerializer(plans, many=True)
        return Response(serializer.data)
