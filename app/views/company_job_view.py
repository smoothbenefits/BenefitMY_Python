from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.company_job import CompanyJob
from app.serializers.company_job_serializer import (
    CompanyJobSerializer,
    CompanyJobPostSerializer)


class CompanyJobView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyJob.objects.get(pk=pk)
        except CompanyJob.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        model = self._get_object(pk)
        serializer = CompanyJobSerializer(model)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        model = self._get_object(pk)
        model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        model = self._get_object(pk)
        serializer = CompanyJobPostSerializer(model, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = CompanyJobPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            response_serializer = CompanyJobSerializer(serializer.object)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyJobByCompanyView(APIView):
    def _get_object(self, company_id):
        try:
            return CompanyJob.objects.filter(company=company_id)
        except CompanyJob.DoesNotExist:
            raise Http404

    def get(self, request, company_id, format=None):
        models = self._get_object(company_id)
        serializer = CompanyJobSerializer(models, many=True)
        return Response(serializer.data)
