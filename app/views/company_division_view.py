from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.company_division import CompanyDivision
from app.serializers.company_division_serializer import (
    CompanyDivisionSerializer,
    CompanyDivisionPostSerializer)


class CompanyDivisionView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyDivision.objects.get(pk=pk)
        except CompanyDivision.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        model = self._get_object(pk)
        serializer = CompanyDivisionSerializer(model)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        model = self._get_object(pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        model = self._get_object(pk)
        serializer = CompanyDivisionPostSerializer(model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = CompanyDivisionPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            response_serializer = CompanyDivisionSerializer(serializer.object)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDivisionByCompanyView(APIView):
    def _get_object(self, company_id):
        try:
            return CompanyDivision.objects.filter(company=company_id)
        except CompanyDivision.DoesNotExist:
            raise Http404

    def get(self, request, company_id, format=None):
        models = self._get_object(company_id)
        serializer = CompanyDivisionSerializer(models, many=True)
        return Response(serializer.data)
