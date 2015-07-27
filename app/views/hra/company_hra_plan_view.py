from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.hra.company_hra_plan import CompanyHraPlan
from app.serializers.hra.company_hra_plan_serializer import (
    CompanyHraPlanSerializer,
    CompanyHraPlanPostSerializer)

class CompanyHraPlanView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyHraPlan.objects.get(pk=pk)
        except CompanyHraPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = CompanyHraPlanSerializer(plan)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = CompanyHraPlanSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = CompanyHraPlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyHraPlanByCompanyView(APIView):
    def _get_object(self, company_id):
        try:
            return CompanyHraPlan.objects.filter(company=company_id)
        except CompanyHraPlan.DoesNotExist:
            raise Http404

    def get(self, request, company_id, format=None):
        plans = self._get_object(company_id)
        serializer = CompanyHraPlanSerializer(plans, many=True)
        return Response(serializer.data)
