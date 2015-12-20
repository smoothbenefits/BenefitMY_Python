from rest_framework.views import APIView
from django.http import Http404
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status

from app.models.hsa.company_group_hsa_plan import CompanyGroupHsaPlan
from app.serializers.hsa.company_group_hsa_plan_serializer import (
    CompanyGroupHsaPlanSerializer, CompanyGroupHsaPlanPostSerializer)


class CompanyGroupHsaPlanByCompanyGroupView(APIView):
    def _get_object_by_group_id(self, group_id):
        try:
            return CompanyGroupHsaPlan.objects.filter(group=group_id)
        except CompanyGroupHsaPlan.DoesNotExist:
            raise Http404

    def get(self, request, group_id, format=None):
        plans = self._get_object_by_group_id(group_id)
        serializer = CompanyGroupHsaPlanSerializer(plans, many=True)
        return Response(serializer.data)

class CompanyGroupHsaPlanByCompanyPlanView(APIView):

    def _get_object(self, pk):
        try:
            return CompanyGroupHsaPlan.objects.get(pk=pk)
        except CompanyGroupHsaPlan.DoesNotExist:
            raise Http404

    def _get_company_group_plan_by_company_plan(self, pk):
        return CompanyGroupHsaPlan.objects.filter(company_hsa_plan=pk)

    def get(self, request, pk, format=None):
        plans = self._get_company_group_plan_by_company_plan(pk)
        serializer = CompanyGroupHsaPlanSerializer(plans, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        plans = self._get_company_group_plan_by_company_plan(pk)
        for plan in plans:
            plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def post(self, request, pk, format=None):
        group_plan_serializer = CompanyGroupHsaPlanPostSerializer(data=request.DATA, many=True)
        if group_plan_serializer.is_valid():
            group_plan_serializer.save()
            return Response(group_plan_serializer.data, status=status.HTTP_201_CREATED)
        return Response(group_plan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def put(self, request, pk, format=None):
        serializer = CompanyGroupHsaPlanSerializer(data=request.DATA, many=True)
        if serializer.is_valid():
            group_plans = self._get_company_group_plan_by_company_plan(pk)
            for plan in group_plans:
                plan.delete()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
