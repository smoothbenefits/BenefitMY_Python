from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.models.hra.company_hra_plan import \
    CompanyHraPlan
from app.models.hra.company_group_hra_plan import \
    CompanyGroupHraPlan
from app.serializers.hra.company_group_hra_plan_serializer import (
    CompanyGroupHraPlanSerializer, 
    CompanyGroupHraPlanPostSerializer)


class CompanyGroupHraPlanByCompanyGroupView(APIView):
    def _get_objects(self, company_group_id):
        return CompanyGroupHraPlan.objects.filter(company_group=company_group_id)

    def get(self, request, company_group_id, format=None):
        plans = self._get_objects(company_group_id)
        serializer = CompanyGroupHraPlanSerializer(plans, many=True)
        return Response(serializer.data)


class CompanyGroupHraPlanByCompanyPlanView(APIView):
    # The 'pk' here is an ID for a company HRA plan

    def _get_company_plan(self, pk):
        try:
            return CompanyHraPlan.objects.get(pk=pk)
        except CompanyHraPlan.DoesNotExist:
            raise Http404

    def _get_company_group_plans(self, comp_plan):
        return CompanyGroupHraPlan.objects.filter(company_hra_plan=comp_plan)

    def get(self, request, pk, format=None):
        comp_plan = self._get_company_plan(pk)
        group_plans = self._get_company_group_plans(comp_plan)
        serializer = CompanyGroupHraPlanSerializer(group_plans, many=True)
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

        serializer = CompanyGroupHraPlanPostSerializer(data=request.DATA, many=True)
        if serializer.is_valid():
            # update by delete and create
            group_plans = self._get_company_group_plans(company_plan)
            for group_plan in group_plans:
                group_plan.delete()
            serializer.save()
            response_serializer = CompanyGroupHraPlanSerializer(serializer.object, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, pk, format=None):
        company_plan = self._get_company_plan(pk)
        serializer = CompanyGroupHraPlanPostSerializer(data=request.DATA, many=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = CompanyGroupHraPlanSerializer(serializer.object, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
