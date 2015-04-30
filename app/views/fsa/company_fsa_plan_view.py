from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.fsa.company_fsa_plan import CompanyFsaPlan
from app.serializers.fsa.company_fsa_plan_serializer import (
    CompanyFsaPlanSerializer, 
    CompanyFsaPlanPostSerializer)


class CompanyFsaPlanView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyFsaPlan.objects.get(pk=pk)
        except CompanyFsaPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = _get_object(pk)
        serializer = CompanyFsaPlanSerializer(plans, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = CompanyFsaPlanSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = CompanyFsaPlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyFsaPlanByCompanyView(APIView):
    def get(self, request, pk, format=None):
        plans = CompanyFsaPlan.objects.filter(company=pk)
        serializer = CompanyFsaPlanSerializer(plans, many=True)
        return Response(serializer.data)