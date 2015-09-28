from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.commuter.company_commuter_plan import CompanyCommuterPlan
from app.serializers.commuter.company_commuter_plan_serializer import (
    CompanyCommuterPlanSerializer,
    CompanyCommuterPlanPostSerializer)


class CompanyCommuterPlanView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyCommuterPlan.objects.get(pk=pk)
        except CompanyCommuterPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = CompanyCommuterPlanSerializer(plan)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = CompanyCommuterPlanSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = CompanyCommuterPlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyCommuterPlanByCompanyView(APIView):
    def _get_object(self, company_id):
        try:
            return CompanyCommuterPlan.objects.filter(company=company_id)
        except CompanyCommuterPlan.DoesNotExist:
            raise Http404

    def get(self, request, company_id, format=None):
        plans = self._get_object(company_id)
        serializer = CompanyCommuterPlanSerializer(plans, many=True)
        return Response(serializer.data)
