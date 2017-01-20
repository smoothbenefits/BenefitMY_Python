from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.company_department import CompanyDepartment
from app.serializers.company_department_serializer import (
    CompanyDepartmentSerializer,
    CompanyDepartmentPostSerializer)


class CompanyDepartmentView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyDepartment.objects.get(pk=pk)
        except CompanyDepartment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        model = self._get_object(pk)
        serializer = CompanyDepartmentSerializer(model)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        model = self._get_object(pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        model = self._get_object(pk)
        serializer = CompanyDepartmentPostSerializer(model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = CompanyDepartmentPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            response_serializer = CompanyDepartmentSerializer(serializer.object)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDepartmentByCompanyView(APIView):
    def _get_object(self, company_id):
        try:
            return CompanyDepartment.objects.filter(company=company_id)
        except CompanyDepartment.DoesNotExist:
            raise Http404

    def get(self, request, company_id, format=None):
        models = self._get_object(company_id)
        serializer = CompanyDepartmentSerializer(models, many=True)
        return Response(serializer.data)
