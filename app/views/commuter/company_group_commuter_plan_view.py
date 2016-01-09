from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.models.commuter.company_commuter_plan import \
    CompanyCommuterPlan
from app.models.commuter.company_group_commuter_plan import \
    CompanyGroupCommuterPlan
from app.serializers.commuter.company_group_commuter_plan_serializer import (
    CompanyGroupCommuterPlanSerializer, 
    CompanyGroupCommuterPlanPostSerializer)


class CompanyGroupCommuterPlanByCompanyGroupView(APIView):
    def _get_objects(self, company_group_id):
        return CompanyGroupCommuterPlan.objects.filter(company_group=company_group_id)

    def get(self, request, company_group_id, format=None):
        plans = self._get_objects(company_group_id)
        serializer = CompanyGroupCommuterPlanSerializer(plans, many=True)
        return Response(serializer.data)


class CompanyGroupCommuterPlanByCompanyPlanView(APIView):
    # The 'pk' here is an ID for a company Commuter plan

    def _get_company_plan(self, pk):
        try:
            return CompanyCommuterPlan.objects.get(pk=pk)
        except CompanyCommuterPlan.DoesNotExist:
            raise Http404

    def _get_company_group_plans(self, comp_plan):
        return CompanyGroupCommuterPlan.objects.filter(company_commuter_plan=comp_plan)

    def get(self, request, pk, format=None):
        comp_plan = self._get_company_plan(pk)
        group_plans = self._get_company_group_plans(comp_plan)
        serializer = CompanyGroupCommuterPlanSerializer(group_plans, many=True)
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

        serializer = CompanyGroupCommuterPlanPostSerializer(data=request.DATA, many=True)
        if serializer.is_valid():
            # update by delete and create
            group_plans = self._get_company_group_plans(company_plan)
            for group_plan in group_plans:
                group_plan.delete()
            serializer.save()
            response_serializer = CompanyGroupCommuterPlanSerializer(serializer.object, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, pk, format=None):
        company_plan = self._get_company_plan(pk)
        serializer = CompanyGroupCommuterPlanPostSerializer(data=request.DATA, many=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = CompanyGroupCommuterPlanSerializer(serializer.object, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
