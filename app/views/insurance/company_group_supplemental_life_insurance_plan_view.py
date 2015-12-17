from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.models.insurance.comp_suppl_life_insurance_plan import \
    CompSupplLifeInsurancePlan
from app.models.insurance.company_group_suppl_life_insurance_plan import \
    CompanyGroupSupplLifeInsurancePlan
from app.serializers.insurance.company_group_supplemental_life_insurance_plan_serializer import (
    CompanyGroupSupplementalLifeInsurancePlanSerializer, 
    CompanyGroupSupplementalLifeInsurancePlanPostSerializer)


class CompanyGroupSupplementalLifeInsurancePlanByCompanyGroupView(APIView):
    def _get_objects(self, company_group_id):
        return CompanyGroupSupplLifeInsurancePlan.objects.filter(company_group=company_group_id)

    def get(self, request, company_group_id, format=None):
        plans = self._get_objects(company_group_id)
        serializer = CompanyGroupSupplementalLifeInsurancePlanSerializer(plans, many=True)
        return Response(serializer.data)


class CompanyGroupSupplementalLifeInsurancePlanByCompanyPlanView(APIView):
    # The 'pk' here is an ID for a company suppl life insurance plan

    def _get_company_plan(self, pk):
        try:
            return CompSupplLifeInsurancePlan.objects.get(pk=pk)
        except CompSupplLifeInsurancePlan.DoesNotExist:
            raise Http404

    def _get_company_group_plans(self, comp_plan):
        return CompanyGroupSupplLifeInsurancePlan.objects.filter(company_suppl_life_insurance_plan=comp_plan)

    def get(self, request, pk, format=None):
        comp_plan = self._get_company_plan(pk)
        group_plans = self._get_company_group_plans(comp_plan)
        serializer = CompanyGroupSupplementalLifeInsurancePlanSerializer(group_plans, many=True)
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

        serializer = CompanyGroupSupplementalLifeInsurancePlanPostSerializer(data=request.DATA, many=True)
        if serializer.is_valid():
            # update by delete and create
            group_plans = self._get_company_group_plans(company_plan)
            for group_plan in group_plans:
                group_plan.delete()
            serializer.save()
            response_serializer = CompanyGroupSupplementalLifeInsurancePlanSerializer(serializer.object, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, pk, format=None):
        company_plan = self._get_company_plan(pk)
        serializer = CompanyGroupSupplementalLifeInsurancePlanPostSerializer(data=request.DATA, many=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = CompanyGroupSupplementalLifeInsurancePlanSerializer(serializer.object, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
