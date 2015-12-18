from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.hsa.company_hsa_plan import CompanyHsaPlan
from app.serializers.hsa.company_hsa_plan_serializer import (
    CompanyHsaPlanSerializer, CompanyHsaPlanPostSerializer)


class CompanyHsaPlanView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyHsaPlan.objects.get(pk=pk)
        except CompanyHsaPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = CompanyHsaPlan.objects.filter(company=pk)
        serializer = CompanyHsaPlanSerializer(plans, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = CompanyHsaPlanSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = CompanyHsaPlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            response_serializer = CompanyHsaPlanSerializer(serializer.object)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyHsaPlanByCompanyView(APIView):
    def _get_plan_by_company(self, company_id):
        return CompanyHsaPlan.objects.filter(company=company_id)

    def get(self, request, company_id, format=None):
        plans = self._get_plan_by_company(company_id)
        serializer = CompanyHsaPlanSerializer(plans, many=True)
        return Response(serializer.data)
