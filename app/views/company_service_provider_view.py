from django.db import transaction
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.models.company_service_provider import CompanyServiceProvider
from app.serializers.company_service_provider_serializer \
    import (
        CompanyServiceProviderSerializer,
        CompanyServiceProviderPostSerializer
    )


class CompanyServiceProviderView(APIView):
    def _get_object(self, pk):
        try:
            return CompanyServiceProvider.objects.get(pk=pk)
        except CompanyServiceProvider.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        entry = self._get_object(pk)
        serializer = CompanyServiceProviderSerializer(entry)
        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        entry = self._get_object(pk)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def put(self, request, pk, format=None):
        entry = self._get_object(pk)
        serializer = CompanyServiceProviderPostSerializer(entry, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, format=None):
        serializer = CompanyServiceProviderPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyServiceProviderByCompanyView(APIView):

    def get(self, request, company_id, format=None):
        entries = CompanyServiceProvider.objects.filter(company=company_id)
        serializer = CompanyServiceProviderSerializer(entries, many=True)
        return Response(serializer.data)
