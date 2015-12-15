from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.models.insurance.company_life_insurance_plan import \
    CompanyLifeInsurancePlan
from app.models.insurance.company_group_basic_life_insurance_plan import \
    CompanyGroupBasicLifeInsurancePlan
from app.serializers.insurance.company_group_basic_life_insurance_plan_serializer import (
    CompanyGroupBasicLifeInsurancePlanSerializer, 
    CompanyGroupBasicLifeInsurancePlanPostSerializer)


class CompanyGroupBasicLifeInsurancePlanByCompanyGroupView(APIView):
    def _get_objects(self, company_group_id):
        return CompanyGroupBasicLifeInsurancePlan.objects.filter(company_group=company_group_id)

    def get(self, request, company_group_id, format=None):
        plans = self._get_objects(company_group_id)
        serializer = CompanyGroupBasicLifeInsurancePlanSerializer(plans, many=True)
        return Response(serializer.data)


class CompanyGroupBasicLifeInsurancePlanByCompanyPlanView(APIView):
    # The 'pk' here is an ID for a company basic life insurance plan

    def _get_company_plan(self, pk):
        try:
            return CompanyLifeInsurancePlan.objects.get(pk=pk)
        except CompanyLifeInsurancePlan.DoesNotExist:
            raise Http404

    def _get_company_group_plans(self, pk):
        return CompanyGroupBasicLifeInsurancePlan.objects.filter(company_basic_life_insurance_plan=pk)

    def get(self, request, pk, format=None):
        group_plans = self._get_company_group_plans(pk)
        serializer = CompanyGroupBasicLifeInsurancePlanSerializer(group_plans, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        group_plans = self._get_company_group_plans(pk)
        for group_plan in group_plans:
            group_plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def put(self, request, pk, format=None):
        company_plan = self._get_company_plan(pk)

        serializer = CompanyGroupBasicLifeInsurancePlanPostSerializer(data=request.DATA, many=True)
        if serializer.is_valid():
            # update by delete and create
            group_plans = self._get_company_group_plans(pk)
            for group_plan in group_plans:
                group_plan.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, pk, format=None):
        company_plan = self._get_company_plan(pk)
        serializer = CompanyGroupBasicLifeInsurancePlanPostSerializer(data=request.DATA, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
