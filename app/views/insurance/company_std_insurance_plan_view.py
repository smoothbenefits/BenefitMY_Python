from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.insurance.company_std_insurance_plan import \
    CompanyStdInsurancePlan
from app.serializers.insurance.company_std_insurance_plan_serializer import (
    CompanyStdInsurancePlanSerializer, CompanyStdInsurancePlanPostSerializer)


class CompanyStdInsurancePlanView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyStdInsurancePlan.objects.get(pk=pk)
        except CompanyStdInsurancePlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = CompanyStdInsurancePlan.objects.filter(company=pk)
        serializer = CompanyStdInsurancePlanSerializer(plans, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = CompanyStdInsurancePlanSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = CompanyStdInsurancePlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
